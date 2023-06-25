from settings import *
from meshes.base_mesh import BaseMesh


class CubeMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.voxel_marker

        self.vbo_format = '2f2 3f2'
        self.attrs = ('in_tex_coord_0', 'in_position',)
        self.vao = self.get_vao()

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='float16')

    def get_vertex_data(self):
        vertices = [
            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1),
            (0, 1, 0), (0, 0, 0), (1, 0, 0), (1, 1, 0)
        ]
        indices = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (1, 6, 7),
            (6, 5, 4), (4, 7, 6),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6)
        ]
        vertex_data = self.get_data(vertices, indices)

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3), (0, 1, 2),
            (0, 2, 3), (0, 1, 2),
            (0, 1, 2), (2, 3, 0),
            (2, 3, 0), (2, 0, 1),
            (0, 2, 3), (0, 1, 2),
            (3, 1, 2), (3, 0, 1),
        ]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data
