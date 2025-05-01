##### Drew's Workshop (WAVEGUIDE BUILDER)#####

# INSTRUCTIONS #####################################
# 1. Start by clicking run on the program
# 2. Input parameters (example inputs below)
#       -Waveguide Type: *select any type
#       -Throat Diameter (in): 1.4
#       -Ref. Frequency (Hz): 2000
#       -Length (in): 2
#       -Horizontal (degrees): 90
#       -Vertical (degrees): 60
#       -Mounting Type: *select any type
#       -Bolt Pattern: *select any type
#       -Thickness (in): 0.25
# 3. Click the "Preview" button to view geometry
# 4. Click the "Export (.stl)" to export to specific file path
####################################################

####################################################
# The purpose of this code is mainly to visualize 
# geometries. The acoustic calculations are very
# basic estimations. Creating the results in real 
# life would more than likely not produce a great 
# sounding loudspeaker
####################################################

# FOR THIS PROJECT I USED TKINTER FOR THE USER INTERFACE
# COMMENTS ARE PROVIDED STEP BY STEP ON HOW THIS WAS CREATED
import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d
import trimesh
import os
from tkinter import filedialog
import time


# SETTING A CLASS FOR THE USER INTERFACE
class UserInterface:

    #THIS INITIATIZES THE WINDOW FOR THE TKINTER INTERFACE
    def __init__(self, root):
        self.root = root
        self.root.title("WAVEGUIDE BUILDER")
        self.root.geometry("765x515")
        self.root.configure(bg="black") 
        self.first_preview_done = False
 
        
        self.MainFrame()

    #THIS IS THE MAIN FRAME THAT HOUSES ALL THE BUTTON AND FRAMES, INCLUDING THE PREVIEW WINDOW
    def MainFrame(self):
        ##### STYLE ########
        border_color = "#D4AF37"
        background_color = "black"
        title_color = "#D4AF37"
        ####################

        # MAIN LABEL FRAME THAT WRAPS AROUND ENTIRE GUI
        self.outerwaveguideFrame = tk.Frame(
            self.root,
            padx=2,
            pady=2,
            bg = border_color,
        )
        self.outerwaveguideFrame.place(x=30, y=60, anchor="nw", width = 700, height = 420)

        self.innerwaveguideFrame = tk.Frame(self.outerwaveguideFrame, bg=background_color)
        self.innerwaveguideFrame.pack(fill="both", expand=True)

        waveguideLabel = tk.Label(root, text="Waveguide Builder", font=("Fixedsys", 16), bg = border_color,fg = background_color)
        waveguideLabel.place(x=30, y=34)  
        ##############################################

        #### WAVEGUIDE TYPE SELECTION ####
        # DROPDOWN SELECTION FOR THE WAVEGUIDE TYPE
        self.waveguideTypeSelection = ["Conical", "Expo Rectagular", "Expo Conical"]
        self.guideTypeEntryLabel = tk.Label(self.innerwaveguideFrame, text="Waveguide Type:", font=("Fixedsys", 10), bg = background_color, fg = border_color)
        self.guideTypeEntryLabel.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # COMBOBOX
        self.style = ttk.Style()

        # SETTING THE THEME OF ALL THE COMBOBOXES
        self.style.theme_create('combostyle', parent='alt', settings={
            'TCombobox': {
                'configure': {
                    'selectbackground': '#A9B8C2',
                    'fieldbackground': '#A9B8C2',
                    'background': '#A9B8C2',
                    'foreground': '#black',
                    'font': ('Fixedsys', 10)
                }
            },

            'TEntry': {
                'configure': {
                    'fieldbackground': '#A9B8C2',  # light yellow field
                    'background': '#A9B8C2',
                    'foreground': '#black',
                    'font': ('Fixedsys', 10)
                }
            }
        })
                
        self.style.theme_use('combostyle')

        self.guideTypecombobox = ttk.Combobox(
            self.innerwaveguideFrame,
            values=self.waveguideTypeSelection,
            state="readonly",
            width=12,
            style="CustomCombobox.TCombobox"  # use the style here
        )
        self.guideTypecombobox.set(self.waveguideTypeSelection[0])
        self.guideTypecombobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ###################################

        #### THROAT SIZE INPUT ####
        # LABEL FOR THE THROAT ENTRY
        self.throatLabel = tk.Label(self.innerwaveguideFrame, text="Throat Diameter (in):", font=("Fixedsys", 10), bg = background_color, fg = border_color)
        self.throatLabel.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        # ENTRY BOX
        self.throatEntryBox = ttk.Entry(self.innerwaveguideFrame, width=14)
        self.throatEntryBox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ########################

        #### REFERENCE FREQUENCY INPUT ####
        # LABEL FOR THE REF FREQUENCY
        self.refFreqEntryLabel = tk.Label(self.innerwaveguideFrame, text="Ref. Frequency (Hz):", font=("Fixedsys", 10), bg = background_color, fg = border_color)
        self.refFreqEntryLabel.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        # ENTRY BOX
        self.refFreqEntryBox = ttk.Entry(self.innerwaveguideFrame, width=14)
        self.refFreqEntryBox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        ###################################

        #### WAVEGUIDE LENGTH INPUT ####
        # LABEL FOR THE LENGTH
        self.lengthEntryLabel = tk.Label(self.innerwaveguideFrame, text="Length (in):", font=("Fixedsys", 10), bg = background_color, fg = border_color)
        self.lengthEntryLabel.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        # ENTRY BOX
        self.lengthEntryBox = ttk.Entry(self.innerwaveguideFrame, width=14)
        self.lengthEntryBox.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        # DATA COLLECTION
        length = self.lengthEntryBox.get()
        #################################

        #### DISPERSION LABEL FRAME ####
        self.outerdispersionFrame = tk.Frame(
            self.innerwaveguideFrame,
            padx=2,
            pady=2,
            bg = border_color,
        )
        self.outerdispersionFrame.place(x=5, y=135, anchor="nw", width = 275, height = 75)
        self.innerdispersionFrame = tk.Frame(self.outerdispersionFrame, bg=background_color)
        self.innerdispersionFrame.pack(fill="both", expand=True)

        dispersion_label = tk.Label(self.root, text="Dispersion", font=("Fixedsys", 13), bg = background_color, fg = title_color)
        dispersion_label.place(x=45, y=185)  
        ################################

        #### HORIZONTAL DISPERSION INPUT ####
        # LABEL FOR THE HOR DISP
        self.horizontalEntryLabel = tk.Label(self.innerdispersionFrame, text="Horizontal (degrees):", font=("Fixedsys", 10), bg = background_color, fg = border_color)
        self.horizontalEntryLabel.grid(row=0, column=0, padx=5, pady=8, sticky="e")
        # ENTRY BOX
        self.horizontalEntryBox = ttk.Entry(self.innerdispersionFrame, width=11)
        self.horizontalEntryBox.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        # DATA COLLECTION
        horizontalDispersion = self.horizontalEntryBox.get()
        ###################################

        #### VETICAL DISPERSION INPUT ####
        # LABEL FOR THE VERT DISP
        self.verticalEntryLabel = tk.Label(self.innerdispersionFrame, text="Vertical (degrees):", font=("Fixedsys", 10), bg = background_color, fg = border_color)
        self.verticalEntryLabel.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        # ENTRY BOX
        self.verticalEntryBox = ttk.Entry(self.innerdispersionFrame, width=11)
        self.verticalEntryBox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ###################################

        #### MOUNTING LABEL FRAME ####
        self.outermountingFrame = tk.Frame(
            self.innerwaveguideFrame,
            padx=2,
            pady=2,
            bg = border_color,
        )
        self.outermountingFrame.place(x=5, y=225, anchor="nw", width = 275, height = 105)
        self.innermountingFrame = tk.Frame(self.outermountingFrame, bg=background_color)
        self.innermountingFrame.pack(fill="both", expand=True)

        mounting_label = tk.Label(self.root, text="Tweeter Mounting", font=("Fixedsys", 13), bg = background_color, fg = title_color)
        mounting_label.place(x=45, y=275)  
        ##############################

        #### MOUNTING INPUT ####
        # LABEL FOR THE MOUNTING TYPE
        self.mountingTypeEntryLabel = tk.Label(self.innermountingFrame, text="Mounting Type:", font=("Fixedsys", 10), bg = background_color, fg = border_color)
        self.mountingTypeEntryLabel.grid(row=0, column=0, padx=5, pady=6, sticky="e")
        # MOUNTING COMBOBOX
        self.mountingTypeSelection = ["None", "Flange"]
        self.mountingTypecombobox = ttk.Combobox(self.innermountingFrame, values=self.mountingTypeSelection, state="readonly", width=16)
        self.mountingTypecombobox.set(self.mountingTypeSelection[0])
        self.mountingTypecombobox.grid(row=0, column=1, padx=5, pady=6, sticky="w")
        ########################


        #### Bolt Pattern INPUT ####
        # LABEL FOR THE BOLT PATTERN
        self.boltEntryLabel = tk.Label(self.innermountingFrame, text="Bolt Pattern:", font=("Fixedsys", 10), bg = background_color, fg = border_color)
        self.boltEntryLabel.grid(row=1, column=0, padx=5, pady=6, sticky="e")
        # BOLT PATTERN COMBOBOX
        self.boltSelection = ["2-Bolt", "4-Bolt"]
        self.boltCombobox = ttk.Combobox(self.innermountingFrame, values=self.boltSelection, state="readonly", width=16)
        self.boltCombobox.set(self.boltSelection[0])
        self.boltCombobox.grid(row=1, column=1, padx=5, pady=6, sticky="w")
        ###################################
        
        #### FLANGE THICKNESS INPUT ####
        # LABEL FOR THE FLANGE THICK
        self.flangeThicknessEntryLabel = tk.Label(self.innermountingFrame, text="Thickness (in):", font=("Fixedsys", 10), bg = background_color, fg = border_color)
        self.flangeThicknessEntryLabel.grid(row=2, column=0, padx=5, pady=6, sticky="e")
        # ENTRY BOX
        self.flangeThicknessEntryBox = ttk.Entry(self.innermountingFrame, width=18)
        self.flangeThicknessEntryBox.grid(row=2, column=1, padx=5, pady=6, sticky="w")
        # DATA COLLECTION
        self.flangeThicknessEntryBox.insert(0, "0.25")
        ###################################
        
        #### Adding Plot to the frame####
        self.add_3d_plot_to_gui()
        #################################

        #### LABEL FOR PREVIEW WIIDOW####
        self.verticalEntryLabel = tk.Label(self.innerwaveguideFrame, text="Preview Window", font=("Fixedsys", 13), bg = border_color, fg = background_color)
        self.verticalEntryLabel.place(x=430, y=5) 
        #################################

        #### PREVIEW BUTTON ####
        self.previewButton = tk.Button(
            self.innerwaveguideFrame,
            text="Preview",
            command=self.collect_inputs,
            bg="#A9B8C2",       
            fg="black",         
            font=("Fixedsys", 15),
            activebackground="#d5d5d5",  
            activeforeground="#556B2F",  
            bd=0,          

            relief="flat",   
            width = 25,
            height=1
        )
        self.previewButton.place(x=12, y=338) 
        ###################################

        #### Export to an .stl BUTTON ####
        self.exportButton = tk.Button(
            self.innerwaveguideFrame,
            text="Export (.stl)",
            command=self.export_current_geometry,
            bg="#8B2500",        
            fg="#D4AF37",  
            font=("Fixedsys", 15),
            activebackground="#d5d5d5", 
            activeforeground="black",  
            bd=0, 
            relief="flat",      
            width = 25,
            height=1
        )
        self.exportButton.place(x=12, y=378) 
        ###################################

    #THIS COLLECTS ALL THE VARIABLES FROM THE BUTTONS AND COMBOBOXES
    def collect_inputs(self):
        try:
            ref_freq = float(self.refFreqEntryBox.get())
            hor_deg = float(self.horizontalEntryBox.get())
            vert_deg = float(self.verticalEntryBox.get())
            D_throat = float(self.throatEntryBox.get()) * 0.0254  # inches to meters
            Length = float(self.lengthEntryBox.get()) * 0.0254   
            flange_thickness = float(self.flangeThicknessEntryBox.get()) * 0.0254 
            waveguide_type = self.guideTypecombobox.get()
            mountType = self.mountingTypecombobox.get()
            boltPattern = self.boltCombobox.get()

            # Generate horn and plot it first
            if waveguide_type == "Conical":
                horn = ConicalHorn(ref_freq, hor_deg, vert_deg, D_throat, Length)
                self.conical_final_plot(D_throat, horn.D_mouth_H, horn.D_mouth_V, Length, flange_thickness, mountType, boltPattern, 
                        flange_outer_diameter=0.12, thickness=0.005, hole_radius=0.003)

            elif waveguide_type == "Expo Conical":
                horn = ExpHorn(ref_freq, hor_deg, vert_deg, D_throat, Length)
                self.exp_conical_final_plot(D_throat, horn.D_mouth_H, horn.D_mouth_V, horn.m_H, horn.m_V, Length, flange_thickness, mountType, boltPattern, 
                        flange_outer_diameter=0.12, thickness=0.005, hole_radius=0.003)
                
            else: 
                horn = ExpHorn(ref_freq, hor_deg, vert_deg, D_throat, Length)
                self.exp_rect_final_plot(D_throat, horn.D_mouth_H, horn.D_mouth_V, horn.m_H, horn.m_V, Length, flange_thickness, mountType, boltPattern, 
                        flange_outer_diameter=0.12, thickness=0.005, hole_radius=0.003)

            horn.display_results()

        except ValueError as e:
            print("Input error:", e)

    #RESAVING THE INPUTS IN ORDER TO EXPORT AS THE .STL
    def export_current_geometry(self):
        try:
            ref_freq = float(self.refFreqEntryBox.get())
            hor_deg = float(self.horizontalEntryBox.get())
            vert_deg = float(self.verticalEntryBox.get())
            D_throat = float(self.throatEntryBox.get()) * 0.0254
            Length = float(self.lengthEntryBox.get()) * 0.0254
            flange_thickness = float(self.flangeThicknessEntryBox.get()) * 0.0254
            waveguide_type = self.guideTypecombobox.get()
            mountType = self.mountingTypecombobox.get()
            boltPattern = self.boltCombobox.get()

            if boltPattern == "4-Bolt":
                bolt_angles = [0, 90, 180, 270]
            elif boltPattern == "2-Bolt":
                bolt_angles = [0, 180]
            else:
                bolt_angles = None

            flange_faces = self.generate_flange(
                D_throat, 0.12, flange_thickness, 0.003, bolt_angles
            ) if mountType == "Flange" else []

            if waveguide_type == "Conical":
                horn = ConicalHorn(ref_freq, hor_deg, vert_deg, D_throat, Length)
                horn_faces, _, _ = self.generate_conical_horn(D_throat, horn.D_mouth_H, horn.D_mouth_V, Length, 0.005)
            elif waveguide_type == "Expo Conical":
                horn = ExpHorn(ref_freq, hor_deg, vert_deg, D_throat, Length)
                horn_faces, _, _ = self.generate_conical_exponential_horn(D_throat, horn.m_H, horn.m_V, Length, 0.005)
            else: 
                horn = ExpHorn(ref_freq, hor_deg, vert_deg, D_throat, Length)
                horn_faces, _, _ = self.generate_rect_exponential_horn(D_throat, horn.m_H, horn.m_V, Length, 0.005)

            all_faces = horn_faces + flange_faces
            self.export_faces_to_stl(all_faces)

        except ValueError as e:
            print("Export error:", e)

    #TRANSFERING THE FACES FOR EXPORTING TO .STL
    def export_faces_to_stl(self, faces, filename="waveguide_export.stl"):
        all_vertices = []
        all_faces = []

        vertex_dict = {}
        index = 0
        for face in faces:
            face_indices = []
            for vertex in face:
                key = tuple(np.round(vertex, 6))  
                if key not in vertex_dict:
                    vertex_dict[key] = index
                    all_vertices.append(vertex)
                    index += 1
                face_indices.append(vertex_dict[key])
            if len(face_indices) == 4: 
                all_faces.append([face_indices[0], face_indices[1], face_indices[2]])
                all_faces.append([face_indices[0], face_indices[2], face_indices[3]])
            elif len(face_indices) == 3:
                all_faces.append(face_indices)

        mesh = trimesh.Trimesh(vertices=np.array(all_vertices), faces=np.array(all_faces))
        
        filepath = filedialog.asksaveasfilename(defaultextension=".stl", filetypes=[("STL files", "*.stl")])
        if filepath:
            mesh.export(filepath)
            print(f"STL exported to: {filepath}")

    #THIS INITIALIZED THE PREVIEW WINDOW TO THE GUI AND IS UPDATED WHEN THE PREVIEW BUTTON IS CLICKED
    def add_3d_plot_to_gui(self):
        self.outerdisplayFrame = tk.Frame(
            self.innerwaveguideFrame,
            padx=2,
            pady=2,
            bg="#D4AF37",
        )
        self.outerdisplayFrame.place(x=285, y=5, width=405, height=405)
        #MATPLOTLIB IS ADDED TO THE WINDOW
        self.fig = Figure(figsize=(5, 5), dpi=100)  
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor("black")
        self.ax.grid(False)
        self.ax.set_axis_off()
        #EMBEDDING THE PLOT TO THE TKINTER WINDOW
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.outerdisplayFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ##### OVERVIEW ON HOW GEOMETRY FUNCTIONS ARE CALLED #####
    #THE FUNCTIONS FOR THE WAVEGUIDES WITH FINAL IN THEM, CALLS THE FLANGE AND WAVEGUIDE FUNCTIONS
    #THE GEOMETRIES ARE COMBINED IN THE FINAL FUNCTIONS ALONG WITH THE SETTINGS

    #THIS FUNCTION IS RESPONSIBLE FOR THE GENERATION OF THE FLANGE, CALLED IN THE WAVEGUIDE GEOMETRY FUNCTIONS
    def generate_flange(self, D_throat, flange_outer_diameter, flange_thickness, hole_radius, bolt_angles_deg, num_radial=100):
        #CREATING PROFILE FOR THE ENTIRE CIRCLE
        theta = np.linspace(0, 2 * np.pi, num_radial)
        cos_t, sin_t = np.cos(theta), np.sin(theta)
        #STARTING ANGLE OF THE 
        x0 = 0
        x1 = -flange_thickness
        r_in = D_throat / 2
        r_out = flange_outer_diameter / 2
        #GENERATING THE 
        flange_inner_front = [(x0, r_in * ct, r_in * st) for ct, st in zip(cos_t, sin_t)]
        flange_inner_back = [(x1, r_in * ct, r_in * st) for ct, st in zip(cos_t, sin_t)]
        flange_outer_front = [(x0, r_out * ct, r_out * st) for ct, st in zip(cos_t, sin_t)]
        flange_outer_back = [(x1, r_out * ct, r_out * st) for ct, st in zip(cos_t, sin_t)]
        #INITIALIZING THE FACES, EMPTY MATRICES
        faces = []
        #KEEP TRACK OF INDEX LOCATION ON THE ING
        def closest_index_on_ring(point, ring):
            dists = [np.linalg.norm(np.array(point[1:]) - np.array(r[1:])) for r in ring]
            return int(np.argmin(dists))
        #USED FOR ADDING THE FACES LATER, INDEXING FOR THE OUTER RIGN
        def use_outer_ring(p):
            dist = np.linalg.norm(np.array(p[1:]))
            return dist > (r_in + r_out) / 2

        all_hole_centers = []
        #CHECKING TO SEE IF THE FACE OVERLAPSE WITH HOLE 
        #DEPENDING ON THE LOCATION OF THE BOLT DETERMINES WHERE THE MESH WILL BE CONNECTED
        #FOR EXAMPLE, THE OUTER RIGN CONNECTS TO THE UPPER PART OF THE HOLE, WHILE THE LOWER IS THE INNER RING
        if bolt_angles_deg is not None:
            for hole_angle_deg in bolt_angles_deg:
                hole_angle = np.deg2rad(hole_angle_deg)
                r_mid = (r_in + r_out) / 2
                hole_center_y = r_mid * np.cos(hole_angle)
                hole_center_z = r_mid * np.sin(hole_angle)
                all_hole_centers.append((hole_center_y, hole_center_z))

                hole_theta = np.linspace(0, 2 * np.pi, num_radial)
                hole_front = [(x0, hole_center_y + hole_radius * np.cos(t),
                                    hole_center_z + hole_radius * np.sin(t)) for t in hole_theta]
                hole_back = [(x1, hole_center_y + hole_radius * np.cos(t),
                                hole_center_z + hole_radius * np.sin(t)) for t in hole_theta]

                for i in range(num_radial - 1):
                    faces.append([hole_back[i], hole_back[i+1], hole_front[i+1], hole_front[i]])

                for i in range(num_radial - 1):
                    p1 = hole_front[i]
                    p2 = hole_front[i+1]
                    if use_outer_ring(p1):
                        q1 = flange_outer_front[closest_index_on_ring(p1, flange_outer_front)]
                        q2 = flange_outer_front[closest_index_on_ring(p2, flange_outer_front)]
                    else:
                        q1 = flange_inner_front[closest_index_on_ring(p1, flange_inner_front)]
                        q2 = flange_inner_front[closest_index_on_ring(p2, flange_inner_front)]
                    faces.append([p1, p2, q2])
                    faces.append([p1, q2, q1])

                for i in range(num_radial - 1):
                    p1b = hole_back[i]
                    p2b = hole_back[i+1]
                    if use_outer_ring(p1b):
                        q1b = flange_outer_back[closest_index_on_ring(p1b, flange_outer_back)]
                        q2b = flange_outer_back[closest_index_on_ring(p2b, flange_outer_back)]
                    else:
                        q1b = flange_inner_back[closest_index_on_ring(p1b, flange_inner_back)]
                        q2b = flange_inner_back[closest_index_on_ring(p2b, flange_inner_back)]
                    faces.append([p2b, p1b, q2b])
                    faces.append([p1b, q1b, q2b])
        #HELPS IDNETIFY OUTER POINTS ON HOLES, COULD BE MADE MORE EFFICIENT BUT THIS IS THE ONLY WAY WE GOT IT TO WORK
        def point_outside_all_holes(y, z):
            return all((y - yc)**2 + (z - zc)**2 > hole_radius**2 for yc, zc in all_hole_centers)
        #THIS IS THE ACTUAL APPENDING OF THE FACES FOR THE FLANGE, EXCLUDING THE MESH OVERLAP OF THE HOLES
        #THE FACE ARE RETURNED
        for i in range(num_radial - 1):
            p1 = flange_inner_front[i]
            p2 = flange_inner_front[i+1]
            p3 = flange_outer_front[i+1]
            p4 = flange_outer_front[i]
            yc = np.mean([p1[1], p2[1], p3[1], p4[1]])
            zc = np.mean([p1[2], p2[2], p3[2], p4[2]])
            if point_outside_all_holes(yc, zc):
                faces.append([p1, p2, p3, p4])

            p1b = flange_outer_back[i]
            p2b = flange_outer_back[i+1]
            p3b = flange_inner_back[i+1]
            p4b = flange_inner_back[i]
            yc = np.mean([p1b[1], p2b[1], p3b[1], p4b[1]])
            zc = np.mean([p1b[2], p2b[2], p3b[2], p4b[2]])
            if point_outside_all_holes(yc, zc):
                faces.append([p1b, p2b, p3b, p4b])

        for i in range(num_radial - 1):
            faces.append([flange_inner_back[i], flange_inner_back[i+1],
                        flange_inner_front[i+1], flange_inner_front[i]])
            faces.append([flange_outer_front[i], flange_outer_front[i+1],
                        flange_outer_back[i+1], flange_outer_back[i]])
        return faces

    def generate_conical_horn(self, D_throat, D_mouth_hor, D_mouth_vert, Length, thickness,
                          num_points=50, num_radial=50, x_offset=0):
    
        x = np.linspace(x_offset, Length + x_offset, num_points)

        half_width_inner = np.linspace(D_throat / 2, D_mouth_hor / 2, num_points)
        half_height_inner = np.linspace(D_throat / 2, D_mouth_vert / 2, num_points)
        half_width_outer = half_width_inner + thickness
        half_height_outer = half_height_inner + thickness

        theta = np.linspace(0, 2 * np.pi, num_radial)
        cos_t, sin_t = np.cos(theta), np.sin(theta)

        vertices_inner, vertices_outer = [], []
        for i in range(num_points):
            xi = x[i]
            hw_i, hh_i = half_width_inner[i], half_height_inner[i]
            hw_o, hh_o = half_width_outer[i], half_height_outer[i]

            inner_profile = [(xi, hh_i * ct, hw_i * st) for ct, st in zip(cos_t, sin_t)]
            outer_profile = [(xi, hh_o * ct, hw_o * st) for ct, st in zip(cos_t, sin_t)]

            vertices_inner.append(inner_profile)
            vertices_outer.append(outer_profile)

        faces = []
        for i in range(num_radial):
            faces.append([vertices_inner[0][i],
                        vertices_inner[0][(i + 1) % num_radial],
                        vertices_outer[0][(i + 1) % num_radial],
                        vertices_outer[0][i]])
            faces.append([vertices_inner[-1][i],
                        vertices_inner[-1][(i + 1) % num_radial],
                        vertices_outer[-1][(i + 1) % num_radial],
                        vertices_outer[-1][i]])

        for i in range(num_points - 1):
            for j in range(num_radial - 1):
                faces.append([vertices_inner[i][j], vertices_inner[i][j + 1],
                            vertices_inner[i + 1][j + 1], vertices_inner[i + 1][j]])
                faces.append([vertices_outer[i][j], vertices_outer[i][j + 1],
                            vertices_outer[i + 1][j + 1], vertices_outer[i + 1][j]])
            
        return faces, vertices_inner, vertices_outer
    
    def generate_conical_exponential_horn(self, D_throat, m_hor, m_vert, L, thickness, num_points=50, num_radial=50):
            #CREATING THE PROFILE POINTS ALONG THE X-AXIS
            x = np.linspace(0, L, num_points)
            half_width_inner = (D_throat / 2) * np.exp(m_vert * x)
            half_height_inner = (D_throat / 2) * np.exp(m_hor * x)
            half_width_outer = half_width_inner + thickness
            half_height_outer = half_height_inner + thickness
            #CIRCULAR CROSS-SECTION GENERATION
            theta = np.linspace(0, 2 * np.pi, num_radial)
            cos_t, sin_t = np.cos(theta), np.sin(theta)
            #GENERATING THE 3D POINTS FOR THE SURFACE
            vertices_inner = []
            vertices_outer = []
            for i in range(num_points):
                xi = x[i]
                hw_i, hh_i = half_width_inner[i], half_height_inner[i]
                hw_o, hh_o = half_width_outer[i], half_height_outer[i]
                
                inner_profile = [(xi, hw_i * ct, hh_i * st) for ct, st in zip(cos_t, sin_t)]
                outer_profile = [(xi, hw_o * ct, hh_o * st) for ct, st in zip(cos_t, sin_t)]
                
                vertices_inner.append(inner_profile)
                vertices_outer.append(outer_profile)
            #CREATION OF THE FRONT AND BACK SURFACES THAT CONNECT THE INNER AND OUTER SURFACE OF THE WAVEGUIDE
            faces = []
            throat_surface = [[vertices_inner[0][i], vertices_inner[0][(i+1) % num_radial], 
                            vertices_outer[0][(i+1) % num_radial], vertices_outer[0][i]] for i in range(num_radial)]
            mouth_surface = [[vertices_inner[-1][i], vertices_inner[-1][(i+1) % num_radial], 
                            vertices_outer[-1][(i+1) % num_radial], vertices_outer[-1][i]] for i in range(num_radial)]
            faces.extend(throat_surface)
            faces.extend(mouth_surface)
            
            #ADDING INNER AND OUTER FACES TO THE SHELL
            for i in range(num_points - 1):
                for j in range(num_radial - 1):
                    faces.append([vertices_inner[i][j], vertices_inner[i][j+1], vertices_inner[i+1][j+1], vertices_inner[i+1][j]])
                    faces.append([vertices_outer[i][j], vertices_outer[i][j+1], vertices_outer[i+1][j+1], vertices_outer[i+1][j]])

            return faces, vertices_inner, vertices_outer
        

    def generate_rect_exponential_horn(self, D_throat, m_hor, m_vert, L, thickness, num_points=50, num_radial=50):
        x = np.linspace(0, L, num_points)

        #PROFILES ALONG THE X-AXIS THAT FOLLOW THE FLARE RATE
        half_width_inner = (D_throat / 2) * np.exp(m_vert * x)
        half_height_inner = (D_throat / 2) * np.exp(m_hor * x)
        half_width_outer = ((D_throat + thickness) / 2) * np.exp(m_vert * x)
        half_height_outer = ((D_throat + thickness) / 2) * np.exp(m_hor * x)
        #CREATION OF VERTICES 
        vertices_inner = []
        vertices_outer = []
        for i in range(num_points):
            hw_i, hh_i, xi = half_width_inner[i], half_height_inner[i], x[i]
            hw_o, hh_o = half_width_outer[i], half_height_outer[i]
            vertices_inner.append([(xi, -hw_i, -hh_i), (xi, hw_i, -hh_i), (xi, hw_i, hh_i), (xi, -hw_i, hh_i)])
            vertices_outer.append([(xi, -hw_o, -hh_o), (xi, hw_o, -hh_o), (xi, hw_o, hh_o), (xi, -hw_o, hh_o)])
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        #ADDING THE FACES ALONG THE SHELL
        faces = []
        for i in range(num_points - 1):
            for j in range(4):
                faces.append([vertices_inner[i][j], vertices_inner[i][(j + 1) % 4], vertices_inner[i + 1][(j + 1) % 4], vertices_inner[i + 1][j]])
                faces.append([vertices_outer[i][j], vertices_outer[i][(j + 1) % 4], vertices_outer[i + 1][(j + 1) % 4], vertices_outer[i + 1][j]])
        #ADDING THE FACES TO CONNECT THE INNER AND OUTER SURFACES
        for j in range(4):
            faces.append([vertices_inner[0][j], vertices_inner[0][(j + 1) % 4], vertices_outer[0][(j + 1) % 4], vertices_outer[0][j]])  
            faces.append([vertices_inner[-1][j], vertices_inner[-1][(j + 1) % 4], vertices_outer[-1][(j + 1) % 4], vertices_outer[-1][j]]) 
        
        return faces, vertices_inner, vertices_outer
        
    #######FOR THE _final_plot FUNCTIONS THE COMMENTS ARE GOING TO BE THE SAME AS THE FIRST ONE
    def conical_final_plot(self, D_throat, D_mouth_hor, D_mouth_vert, Length, flange_thickness,mountType, boltPattern, 
                        flange_outer_diameter, thickness, hole_radius):
        #REMOVING THE EXISTING AXIS
        self.ax.clear()
        #TAKING THE USERS INPUTS TO IMPLEMENT THE BOLT PATTERN
        if boltPattern == "4-Bolt":
            bolt_angles = [0, 90, 180, 270]
        elif boltPattern == "2-Bolt":
            bolt_angles = [0, 180]
        else:
            bolt_angles = None
        #CALLING THE FUNCTIONS TO GENERATE THE HORN AND THE FLANGE
        horn_faces, _, _ = self.generate_conical_horn(D_throat, D_mouth_hor, D_mouth_vert, Length, thickness)
        flange_faces = self.generate_flange(D_throat, flange_outer_diameter, flange_thickness, hole_radius, bolt_angles)
        #ADDING THE PLOT TO THE HORN
        self.ax.add_collection3d(Poly3DCollection(horn_faces, facecolor='black', edgecolor='#D4AF37', linewidths=.5, alpha=1))
        #OPTION OF PLOTTING THE FLANGE
        if mountType in ["Flange"]:
            self.ax.add_collection3d(Poly3DCollection(flange_faces, facecolor='black', edgecolor='#D4AF37', linewidths=.5, alpha=1))
        #THIS IS JUST THE ADJUSTMENT OF THE PLOTS
        r_outer = flange_outer_diameter / 2
        max_dim = max(r_outer, D_mouth_hor / 2, D_mouth_vert / 2) * 1.1 
        #PLOT SETUP
        self.ax.set_ylim(-max_dim, max_dim)
        self.ax.set_ylim(-max_dim, max_dim)
        self.ax.set_zlim(-max_dim, max_dim)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        x_span = max_dim * 1
        y_span = max_dim * 1
        z_span = max_dim * 1
        self.ax.set_box_aspect([x_span, y_span, z_span])
        self.ax.set_facecolor("black")     
        self.ax.grid(False)    
        self.ax.set_axis_off()           
        #RE-UPLOADING PLOT TO GUI
        self.canvas.draw()

    def exp_conical_final_plot(self, D_throat, D_mouth_hor, D_mouth_vert, m_hor,m_vert, Length, flange_thickness,mountType, boltPattern, 
                        flange_outer_diameter, thickness, hole_radius):

        self.ax.clear()

        if boltPattern == "4-Bolt":
            bolt_angles = [0, 90, 180, 270]
        elif boltPattern == "2-Bolt":
            bolt_angles = [0, 180]
        else:
            bolt_angles = None

        horn_faces, _, _ = self.generate_conical_exponential_horn(D_throat, m_hor, m_vert, Length, thickness, num_points=50, num_radial=50)

        flange_faces = self.generate_flange(D_throat, flange_outer_diameter, flange_thickness, hole_radius, bolt_angles)

        self.ax.add_collection3d(Poly3DCollection(horn_faces, facecolor='black', edgecolor='#D4AF37', linewidths=.5, alpha=1))

        if mountType in ["Flange"]:
            self.ax.add_collection3d(Poly3DCollection(flange_faces, facecolor='black', edgecolor='#D4AF37', linewidths=.5, alpha=1))

        r_outer = flange_outer_diameter / 2
        max_dim = max(r_outer, D_mouth_hor / 2, D_mouth_vert / 2) * 1.1 

        self.ax.set_ylim(-max_dim, max_dim)
        self.ax.set_ylim(-max_dim, max_dim)
        self.ax.set_zlim(-max_dim, max_dim)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        x_span = max_dim * 1
        y_span = max_dim * 1
        z_span = max_dim * 1
        self.ax.set_box_aspect([x_span, y_span, z_span])
        self.ax.set_facecolor("black")  
        self.ax.grid(False)            
        self.ax.set_axis_off()          
        self.canvas.draw()

    def exp_rect_final_plot(self, D_throat, D_mouth_hor, D_mouth_vert, m_hor,m_vert, Length, flange_thickness,mountType, boltPattern, 
                        flange_outer_diameter, thickness, hole_radius):

        self.ax.clear()

        if boltPattern == "4-Bolt":
            bolt_angles = [0, 90, 180, 270]
        elif boltPattern == "2-Bolt":
            bolt_angles = [0, 180]
        else:
            bolt_angles = None

        horn_faces, _, _ = self.generate_rect_exponential_horn(D_throat, m_hor, m_vert, Length, thickness, num_points=50, num_radial=50)
        flange_faces = self.generate_flange(D_throat, flange_outer_diameter, flange_thickness, hole_radius, bolt_angles)

        self.ax.add_collection3d(Poly3DCollection(horn_faces, facecolor='black', edgecolor='#D4AF37', linewidths=.5, alpha=1))

        if mountType in ["Flange"]:
            self.ax.add_collection3d(Poly3DCollection(flange_faces, facecolor='black', edgecolor='#D4AF37', linewidths=.5, alpha=1))

        r_outer = flange_outer_diameter / 2
        max_dim = max(r_outer, D_mouth_hor / 2, D_mouth_vert / 2) * 1.1 

        self.ax.set_ylim(-max_dim, max_dim)
        self.ax.set_ylim(-max_dim, max_dim)
        self.ax.set_zlim(-max_dim, max_dim)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        x_span = max_dim * 1
        y_span = max_dim * 1
        z_span = max_dim * 1
        self.ax.set_box_aspect([x_span, y_span, z_span])
        self.ax.set_facecolor("black")    
        self.ax.grid(False)              
        self.ax.set_axis_off()           

        self.canvas.draw()

    def on_selection_change(self, event):
        selected = self.combobox.get()
        self.label_result.config(text=f"You selected: {selected}")


#THESE CLASSES ARE BASICALLY ALL THE ACOUSTIC CALCULATIONS FOR EACH OF THE TYPES OF HORNS
#THE CONICAL EXPONENTIAL FALLS UNDER THE ExpHorn CLASS, BUT BASICALLY IS A COMBO OF THE TWO TYPES OF WAVEGUIDES
class ExpHorn:
    def __init__(self, ref_freq, hor_deg, vert_deg, D_throat, Length, k=60):
        self.ref_freq = ref_freq
        self.hor_deg = hor_deg
        self.vert_deg = vert_deg
        self.D_throat = D_throat
        self.Length = Length
        self.k = k
        self.c = 343  
        # FINDING THE DIAMTERS FOR THE OUTLET MOUTH, CALLS FUNCTION BELOW
        self.D_mouth_H = self._calculate_mouth_diameter(self.hor_deg)
        self.D_mouth_V = self._calculate_mouth_diameter(self.vert_deg)
        # CALCULATING FLARE CONSTANT
        self.m_H = self._calculate_flare_constant(self.D_mouth_H)
        self.m_V = self._calculate_flare_constant(self.D_mouth_V)
        # COMPUTING CUTOFF FREQUENCIES
        self.fc_H, self.fc_V, self.fc_eff = self._calculate_cutoff_frequencies()

    def _calculate_mouth_diameter(self, directivity_angle_deg):
        return (self.k * self.c) / (self.ref_freq * directivity_angle_deg)

    def _calculate_flare_constant(self, D_mouth):
        return (1 / self.Length) * np.log(D_mouth / self.D_throat)

    def _calculate_cutoff_frequencies(self):
        fc_H = (self.m_H * self.c) / (4 * np.pi)
        fc_V = (self.m_V * self.c) / (4 * np.pi)
        fc_eff = max(fc_H, fc_V) 
        return fc_H, fc_V, fc_eff
    #THIS WAS USED FOR DEBUGGING IN THE INITIAL WORK
    def display_results(self):
        print("=== Exponential Horn Parameters ===")
        print(f"Reference Frequency: {self.ref_freq} Hz")
        print(f"Throat Diameter: {self.D_throat:.3f} m")
        print(f"Horn Length: {self.Length:.3f} m")
        print(f"Horizontal Mouth Diameter: {self.D_mouth_H:.3f} m")
        print(f"Vertical Mouth Diameter: {self.D_mouth_V:.3f} m")
        print(f"Horizontal Flare Constant: {self.m_H:.3f} m^-1")
        print(f"Vertical Flare Constant: {self.m_V:.3f} m^-1")
        print(f"Horizontal Cutoff Frequency: {self.fc_H:.2f} Hz")
        print(f"Vertical Cutoff Frequency: {self.fc_V:.2f} Hz")
        print(f"Effective Practical Cutoff Frequency: {self.fc_eff:.2f} Hz")

class ConicalHorn:
    def __init__(self, ref_freq, hor_deg, vert_deg, D_throat, Length, k=60):
        self.ref_freq = ref_freq
        self.hor_deg = hor_deg
        self.vert_deg = vert_deg
        self.D_throat = D_throat
        self.Length = Length
        self.k = k
        self.c = 343
        # FINDING THE DIAMTERS FOR THE OUTLET MOUTH, CALLS FUNCTION BELOW
        self.D_mouth_H = self._calculate_mouth_diameter(self.hor_deg)
        self.D_mouth_V = self._calculate_mouth_diameter(self.vert_deg)

    def _calculate_mouth_diameter(self, directivity_angle_deg):
        return (self.k * self.c) / (self.ref_freq * directivity_angle_deg)
    #THIS WAS USED FOR DEBUGGING IN THE INITIAL WORK
    def display_results(self):
        print("=== Conical Horn Parameters ===")
        print(f"Reference Frequency: {self.ref_freq} Hz")
        print(f"Throat Diameter: {self.D_throat:.3f} m")
        print(f"Horn Length: {self.Length:.3f} m")
        print(f"Horizontal Mouth Diameter: {self.D_mouth_H:.3f} m")
        print(f"Vertical Mouth Diameter: {self.D_mouth_V:.3f} m")

#THIS RUNS THE APPLICATION
if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()


