from settings import *
from meshes.base_mesh import BaseMesh
from noise import *


class CloudMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.ctx = self.app.ctx
        self.program = self.app.shader_program.clouds
        self.vbo_format = '3u2'
        self.attrs = ('in_position',)
        self.vao = self.get_vao()

    def get_vertex_data(self):
        cloud_data = np.zeros(WORLD_AREA * CHUNK_SIZE ** 2, dtype='uint8')
        self.gen_clouds(cloud_data)

        return self.build_mesh(cloud_data)

    @staticmethod
    @njit
    def gen_clouds(cloud_data):
        for x in range(WORLD_W * CHUNK_SIZE):
            for z in range(WORLD_D * CHUNK_SIZE):

                if noise2(0.13 * x, 0.13 * z) < 0.2:
                    continue
                cloud_data[x + WORLD_W * CHUNK_SIZE * z] = 1

    @staticmethod
    @njit
    def build_mesh(cloud_data):
        mesh = np.empty(WORLD_AREA * CHUNK_AREA * 6 * 3, dtype='uint16')
        index = 0
        width = WORLD_W * CHUNK_SIZE
        depth = WORLD_D * CHUNK_SIZE

        y = CLOUD_HEIGHT
        visited = set()

        for z in range(depth):
            for x in range(width):

                idx = x + width * z
                if not cloud_data[idx] or idx in visited:
                    continue

                # find number of continuous quads along x
                x_count = 1
                idx = (x + x_count) + width * z
                while x + x_count < width and cloud_data[idx] and idx not in visited:
                    x_count += 1
                    idx = (x + x_count) + width * z

                # find the number of continuous quads along z for each x
                z_count_list = []
                for ix in range(x_count):
                    z_count = 1
                    idx = (x + ix) + width * (z + z_count)
                    while (z + z_count) < depth and cloud_data[idx] and idx not in visited:
                        z_count += 1
                        idx = (x + ix) + width * (z + z_count)
                    z_count_list.append(z_count)

                # find min count z to form a large quad
                z_count = min(z_count_list) if z_count_list else 1

                # mark all unit quads of the large quad as visited
                for ix in range(x_count):
                    for iz in range(z_count):
                        visited.add((x + ix) + width * (z + iz))

                v0 = x, y, z
                v1 = x + x_count, y, z + z_count
                v2 = x + x_count, y, z
                v3 = x, y, z + z_count

                for vertex in (v0, v1, v2, v0, v3, v1):
                    for attr in vertex:
                        mesh[index] = attr
                        index += 1

        mesh = mesh[:index + 1]
        return mesh
