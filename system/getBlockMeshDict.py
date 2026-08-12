import numpy as np
import matplotlib.pyplot as plt
import blocktool as blt

def generate_blockMeshDict(rows=2, cols=30, skip=1, radius=0.0125, spacing=0.04, zmax=1.4, nz=70, nt=4):
    mesh = blt.Mesh(0, zmax, nz)

    nrows = 2*rows*(1+skip)
    ncols = cols*(1+skip) - skip
    dy = spacing / 2.0
    l = spacing / np.sqrt(3)    # side length of hexagon
    dx = 1.5*l
    R = radius
    r = 0.8*R

    print(f"Cylinder density = {2/np.sqrt(3)/(spacing*(skip+1))**2}")
    print("Generating mesh...")
    
    # build base grid verts 
    vgrid = []
    for i in range(nrows + 1):
        y = i * dy
        irow = [mesh.add_vert(-spacing, y)] 
        for j in range(ncols + 1):
            x = -l + j*dx + (i+j)%2*l/2
            v = mesh.add_vert(x, y)
            irow.append(v)
        irow.append(mesh.add_vert(ncols*dx, y))
        vgrid.append(irow)

    # subdivide edge for cylinders
    cdict = {}
    even_col = False
    for j in range(1, len(vgrid[0])-2, skip+1):
        for i in range(even_col*(skip+1), len(vgrid), 2*(skip+1)):
            x = vgrid[i][j].x + l
            y = vgrid[i][j].y
            cdict[vgrid[i][j]] = [mesh.add_vert(x-R,y), mesh.add_vert(x-r,y), mesh.add_vert(x+r,y), mesh.add_vert(x+R,y)]
        even_col = not even_col
    print(f"Number of cylinders = {len(cdict)}")
    print(f"Last cylinder location = ({x}, {y})")

    # create blocks
    for i in range(len(vgrid)-1):
        for j in range(len(vgrid[0])-1):
            v0 = vgrid[i][j]
            v1 = vgrid[i][j+1]
            v2 = vgrid[i+1][j+1]
            v3 = vgrid[i+1][j]
            if v0 in cdict.keys():
                s0, s1, s2, s3 = cdict[v0]
                x0 = 0.5*(v0.x + v1.x)
                y0 = v0.y
                u0 = mesh.add_vert(r*np.cos(np.deg2rad(120))+x0, r*np.sin(np.deg2rad(120))+y0)
                u1 = mesh.add_vert(r*np.cos(np.deg2rad(60))+x0,  r*np.sin(np.deg2rad(60))+y0)
                u2 = mesh.add_vert(R*np.cos(np.deg2rad(60))+x0,  R*np.sin(np.deg2rad(60))+y0)
                u3 = mesh.add_vert(R*np.cos(np.deg2rad(120))+x0, R*np.sin(np.deg2rad(120))+y0)
                mesh.add_block(s1, s2, u1, u0, ny=nt, nx=nt)
                mesh.add_block(u1, s2, s3, u2, ny=1, nx=nt)
                mesh.add_block(u0, u1, u2, u3, ny=1, nx=nt)
                mesh.add_block(s1, u0, u3, s0, ny=1, nx=nt)
                mesh.add_block(u2, s3, v1, v2, gy=2, nx=nt)
                mesh.add_block(u3, u2, v2, v3, gy=2, nx=nt)
                mesh.add_block(s0, u3, v3, v0, gy=2, nx=nt)
                # edges
                mesh.add_edge(s3, u2, R*np.cos(np.deg2rad(30))+x0, R*np.sin(np.deg2rad(30))+y0)
                mesh.add_edge(u2, u3, R*np.cos(np.deg2rad(90))+x0, R*np.sin(np.deg2rad(90))+y0)
                mesh.add_edge(u3, s0, R*np.cos(np.deg2rad(150))+x0, R*np.sin(np.deg2rad(150))+y0)
                if skip > 0:
                    mesh.add_edge(v1, v2, l*np.cos(np.deg2rad(30))+x0, l*np.sin(np.deg2rad(30))+y0)
                    mesh.add_edge(v2, v3, l*np.cos(np.deg2rad(90))+x0, l*np.sin(np.deg2rad(90))+y0)
                    mesh.add_edge(v3, v0, l*np.cos(np.deg2rad(150))+x0, l*np.sin(np.deg2rad(150))+y0)
            elif v3 in cdict.keys():
                s0, s1, s2, s3 = cdict[v3]
                x0 = 0.5*(v0.x + v1.x)
                y0 = v3.y
                u0 = mesh.add_vert(R*np.cos(np.deg2rad(240))+x0, R*np.sin(np.deg2rad(240))+y0)
                u1 = mesh.add_vert(R*np.cos(np.deg2rad(300))+x0, R*np.sin(np.deg2rad(300))+y0)
                u2 = mesh.add_vert(r*np.cos(np.deg2rad(300))+x0, r*np.sin(np.deg2rad(300))+y0)
                u3 = mesh.add_vert(r*np.cos(np.deg2rad(240))+x0, r*np.sin(np.deg2rad(240))+y0)
                mesh.add_block(u3, u2, s2, s1, ny=nt, nx=nt)
                mesh.add_block(u3, s1, s0, u0, ny=1, nx=nt)
                mesh.add_block(u2, u3, u0, u1, ny=1, nx=nt)
                mesh.add_block(s2, u2, u1, s3, ny=1, nx=nt)
                mesh.add_block(u0, s0, v3, v0, gy=2, nx=nt)
                mesh.add_block(u1, u0, v0, v1, gy=2, nx=nt)
                mesh.add_block(s3, u1, v1, v2, gy=2, nx=nt)
                # edges
                mesh.add_edge(s0, u0, R*np.cos(np.deg2rad(210))+x0, R*np.sin(np.deg2rad(210))+y0)
                mesh.add_edge(u0, u1, R*np.cos(np.deg2rad(270))+x0, R*np.sin(np.deg2rad(270))+y0)
                mesh.add_edge(u1, s3, R*np.cos(np.deg2rad(330))+x0, R*np.sin(np.deg2rad(330))+y0)
                if skip > 0:
                    mesh.add_edge(v3, v0, l*np.cos(np.deg2rad(210))+x0, l*np.sin(np.deg2rad(210))+y0)
                    mesh.add_edge(v0, v1, l*np.cos(np.deg2rad(270))+x0, l*np.sin(np.deg2rad(270))+y0)
                    mesh.add_edge(v1, v2, l*np.cos(np.deg2rad(330))+x0, l*np.sin(np.deg2rad(330))+y0)
            else:
                mesh.add_block(v0, v1, v2, v3, nx=nt, ny=nt)

    # downscale resolution
    # mesh.scale_resolution(2, 2, 1)

    # create patch 
    vfront = []
    for v in vgrid[0]:
        vfront.append(v)
        if v in cdict.keys():
            vfront.extend(cdict[v])
    vback = []
    for v in vgrid[-1]:
        vback.append(v)
        if v in cdict.keys():
            vback.extend(cdict[v])
    # mesh.add_patch("front", "symmetryPlane", vfront)
    # mesh.add_patch("back", "symmetryPlane", vback)
    mesh.add_patch("front", "cyclic;\n\tneighbourPatch back", vfront)
    mesh.add_patch("back", "cyclic;\n\tneighbourPatch front", vback)
    mesh.add_patch("interface3", "patch", [vgrid[i][0] for i in range(len(vgrid))])
    mesh.add_patch("interface4", "patch", [vgrid[i][-1] for i in range(len(vgrid))])

    # buffer block
    x0 = vgrid[-1][0].x
    y0 = vgrid[-1][0].y
    x1 = vgrid[-1][-1].x
    mesh.new_box(-1, 0, -0.1, y0, "front", "interface0", "back", "inlet", dx=0.02, dy=0.02)
    mesh.new_box(-0.1, 0, x0, y0, "front", "interface2", "back", "interface1", dx=0.01, dy=0.01)
    mesh.new_box(x1, 0, x0+x1+0.1, y0, "front", "interface6", "back", "interface5", dx=0.01, dy=0.01)
    mesh.new_box(x0+x1+0.1, 0, x0+x1+3, y0, "front", "outlet", "back", "interface7", dx=0.02, dy=0.02)

    print(f"Vert count = {len(mesh.verts)}")
    print(f"Cell count = {mesh.get_cell_count()}")

    mesh.add_patchpair(mesh.patches["interface0"], mesh.patches["interface1"])
    mesh.add_patchpair(mesh.patches["interface2"], mesh.patches["interface3"])
    mesh.add_patchpair(mesh.patches["interface4"], mesh.patches["interface5"])
    mesh.add_patchpair(mesh.patches["interface6"], mesh.patches["interface7"])

    mesh.show_blocks()

    with open("system/blockMeshDict", "w") as file:
        file.write(mesh.write_all())


def unit_cylinder(r=0.0125, n=24):
    
    th = np.linspace(0, 2*np.pi, n, endpoint=False)
    x = r * np.cos(th)
    y = r * np.sin(th)

    vertices = []
    triangles = []

    for i in range(n):
        vertices.append((x[i], y[i], 0.0))
        vertices.append((x[i], y[i], 1.0))

    bottom_center_index = len(vertices)
    vertices.append((0.0, 0.0, 0.0)) 
    top_center_index = len(vertices)
    vertices.append((0.0, 0.0, 1.0))

    # sides
    for i in range(n):
        ip1 = (i + 1) % n
        b0 = 2*i
        t0 = 2*i + 1
        b1 = 2*ip1
        t1 = 2*ip1 + 1
        triangles.append((b0, b1, t1))
        triangles.append((b0, t1, t0))

    # botom cap
    for i in range(n):
        ip1 = (i + 1) % n
        b0 = 2*i
        b1 = 2*ip1
        triangles.append((bottom_center_index, b1, b0))

    # top cap
    for i in range(n):
        ip1 = (i + 1) % n
        t0 = 2*i + 1
        t1 = 2*ip1 + 1
        triangles.append((top_center_index, t0, t1))

    return np.array(vertices), np.array(triangles)

def transform(verts, x, y, height):
    new_verts = verts.copy()
    new_verts[:,0] += x
    new_verts[:,1] += y
    new_verts[:,2] *= height
    return new_verts

def write_stl(filename, vertices, triangles):
    with open(filename, "w") as f:
        f.write("solid cylinders\n")
        for tri in triangles:
            p1, p2, p3 = vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]
            n = np.cross(p2 - p1, p3 - p1)
            r = np.linalg.norm(n)
            if r > 0:
                n /= r
            f.write(f"  facet normal {n[0]} {n[1]} {n[2]}\n")
            f.write("    outer loop\n")
            f.write(f"      vertex {p1[0]} {p1[1]} {p1[2]}\n")
            f.write(f"      vertex {p2[0]} {p2[1]} {p2[2]}\n")
            f.write(f"      vertex {p3[0]} {p3[1]} {p3[2]}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        f.write("endsolid cylinders\n")
        
def cylinder_array(x, y, height, r=0.0125, n=24):
    unit_vertices, unit_triangles = unit_cylinder(r, n)

    all_vertices = []
    all_triangles = []
    offset = 0
    
    for i in range(len(x)):
        transformed_vertices = transform(unit_vertices, x[i], y[i], height[i])
        all_vertices.append(transformed_vertices)
        all_triangles.append(unit_triangles + offset)
        offset += len(transformed_vertices)
        
    all_vertices = np.vstack(all_vertices)
    all_triangles = np.vstack(all_triangles)

    return all_vertices, all_triangles

def generate_stl(b=1.6, seed=42, rows=6, cols=30, skip=1, radius=0.0125, spacing=0.04):

    np.random.seed(seed)
    dy = spacing * (skip+1)
    dx = dy * 0.5 * np.sqrt(3)

    x = []
    y = []
    height = []
    for j in range(rows):
        for i in range(cols):
            x.append(i * dx) 
            y.append(dy * (j + 0.5*(i%2)))
            
            if b > 0:
                h = np.random.exponential(1/b)
            else:
                h = 2.0 
            height.append(h)

            if j == 0 and (i % 2) == 0:
                x.append(i * dx)
                y.append(dy * rows)
                height.append(h)
            
    # plt.plot(x, y, ".")
    # plt.axis("equal")

    vertices, triangles = cylinder_array(x, y, height)
    write_stl("constant/triSurface/mySurface.stl", vertices, triangles)

if __name__ == "__main__":

    ZMAX = 0.8
    NZ = np.round(ZMAX / 0.02)
    ROWS = 6
    COLS = 20
    SEED = 42
    B1 = 1.7

    generate_stl(B1, SEED, ROWS, COLS)
    generate_blockMeshDict(ROWS, COLS, zmax=ZMAX, nz=NZ)
