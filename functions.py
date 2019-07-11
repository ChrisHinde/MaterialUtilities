import bpy

def mu_assign_material_slots(object, material_list):
    """Given an object and a list of material names removes all material slots from the object
       adds new ones for each material in the material list, adds the materials to the slots as well."""

    scene = bpy.context.scene
    active_object = bpy.context.active_object
    bpy.context.view_layer.objects.active = object

    for s in object.material_slots:
        bpy.ops.object.material_slot_remove()

    # re-add them and assign material
    i = 0
    for mat in material_list:
        material = bpy.data.materials[mat]
        object.data.materials.append(material)
        i += 1

    # restore active object:
    bpy.context.view_layer.objects.active = active_object

def mu_assign_to_data(object, material, index, edit_mode, all = True):
    """Assign the material to the object data (polygons/splines)"""

    if object.type == 'MESH':
        # now assign the material to the mesh
        mesh = object.data
        if all:
            for poly in mesh.polygons:
                poly.material_index = index
        else:
            for poly in mesh.polygons:
                if poly.select:
                    poly.material_index = index

        mesh.update()

    elif object.type in {'CURVE', 'SURFACE', 'TEXT'}:
        bpy.ops.object.mode_set(mode = 'EDIT')    # This only works in Edit mode

        # If operator was run in Object mode
        if not edit_mode:
            # Select everything in Edit mode
            bpy.ops.curve.select_all(action = 'SELECT')

        bpy.ops.object.material_slot_assign()   # Assign material of the current slot to selection

        if not edit_mode:
            bpy.ops.object.mode_set(mode = 'OBJECT')


def mu_assign_material(self, material_name = "Default", override_type = 'APPEND_MATERIAL'):
    """Assign the defined material to selected polygons/objects"""

    print("ASSMat: " + material_name + " : " + override_type)

    # get active object so we can restore it later
    active_object = bpy.context.active_object

    edit_mode = False
    all_polygons = True
    if active_object.mode == 'EDIT':
        edit_mode = True
        all_polygons = False
        bpy.ops.object.mode_set()

    # check if material exists, if it doesn't then create it
    found = False
    for material in bpy.data.materials:
        if material.name == material_name:
            target = material
            found = True
            break

    if not found:
        target = bpy.data.materials.new(material_name)
        target.use_nodes = True         # When do we not want nodes today?


    index = 0
    objects = bpy.context.selected_editable_objects

    for obj in objects:
        # set the active object to our object
        scene = bpy.context.scene
        bpy.context.view_layer.objects.active = obj

        # If we should override all current material slots
        if override_type == 'OVERRIDE_ALL' or obj.type == 'META':
            # Clear out the material slots
            obj.data.materials.clear()
            # and then append the target material
            obj.data.materials.append(target)

            # Assign the material to the data/palys, to avoid weird problems
            mu_assign_to_data(obj, target, 0, edit_mode, True)

            if obj.type == 'META':
                self.report({'INFO'}, "Meta balls only support one material, all other materials overriden!")

        # If we should override each material slot
        elif override_type == 'OVERRIDE_SLOTS':
            i = 0
            # go through each slot
            for material in obj.material_slots:
                # assign the target material to current slot
                obj.data.materials[i] = target
                i += 1

        # if we should keep the material slots and just append the selected material (if not already assigned)
        elif override_type == 'APPEND_MATERIAL':
            found = False
            i = 0
            material_slots = obj.material_slots

            # check material slots for material_name materia
            for material in material_slots:
                if material.name == material_name:
                    found = True
                    index = i
                    # make slot active
                    obj.active_material_index = i
                    break
                i += 1

            if not found:
                # the material is not attached to the object
                if (len(obj.data.materials) == 1) and not edit_mode:
                    # in object mode, override the material if it's just one slot used
                    obj.data.materials[0] = target
                    index = 0
                else:
                    # In Edit mode, or if there's not a slot, append the assigned material
                    #  If we're overriding, there's currently no materials at all, so after this there will be 1
                    #  If not, this adds another slot with the assigned material
                    index = len(obj.data.materials)
                    obj.data.materials.append(target)
                    obj.active_material_index = index

                mu_assign_to_data(obj, target, index, edit_mode, all_polygons)

    #restore the active object
    bpy.context.view_layer.objects.active = active_object

    if edit_mode:
        bpy.ops.object.mode_set(mode='EDIT')

    print("End of Assign material!")
    return {'FINISHED'}


def mu_select_by_material_name(self, find_material_name, extend_selection = False):
    """Searches through all objects, or the polygons/curves of the current object
    to find and select objects/data with the desired material"""

    # in object mode selects all objects with material find_material_name
    # in edit mode selects all polygons with material find_material_name

    find_material = bpy.data.materials.get(find_material_name)

    if find_material is None:
        self.report({'INFO'}, "The material " + find_material_name + " doesn't exists!")
        return {'CANCELLED'}

    # check for edit_mode
    edit_mode = False
    found_material = False

    scene = bpy.context.scene

    # set selection mode to polygons
    scene.tool_settings.mesh_select_mode = False, False, True

    active_object = bpy.context.active_object

    if active_object.mode == 'EDIT':
        edit_mode = True

    if not edit_mode:
        objects = bpy.data.objects
        for obj in objects:
            if obj.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}:
                mat_slots = obj.material_slots
                for material in mat_slots:
                    if material.material == find_material:
                        obj.select_set(state = True)

                        found_material = True

                        # the active object may not have the material!
                        # set it to one that does!
                        bpy.context.view_layer.objects.active = obj
                        break
                    else:
                        if not extend_selection:
                            obj.select_set(state=False)

            #deselect non-meshes
            elif not extend_selection:
                obj.select_set(state=False)

        if not found_material:
            self.report({'INFO'}, "No objects found with the material " + find_material_name + "!")
            return {'CANCELLED'}

    else:
        # it's edit_mode, so select the polygons

        obj = active_object

        if obj.type == 'MESH':
            # if not extending the selection, deselect all first
            #  (Without this, edges/faces were still selected
            #   while the faces were deselcted)
            if not extend_selection:
                bpy.ops.mesh.select_all(action = 'DESELECT')

            bpy.ops.object.mode_set()

            mat_slots = obj.material_slots

            # same material can be on multiple slots
            slot_indeces = []
            i = 0
            for material in mat_slots:
                if material.material == find_material:
                    slot_indeces.append(i)
                i += 1

            mesh = obj.data

            for poly in mesh.polygons:
                if poly.material_index in slot_indeces:
                    poly.select = True
                    found_material = True
                elif not extend_selection:
                    poly.select = False

            mesh.update()

            bpy.ops.object.mode_set(mode = 'EDIT')

            if not found_material:
                self.report({'INFO'}, "Material " + find_material_name + " isn't assigned to any faces!")
                return {'CANCELLED'}

        elif obj.type in {'CURVE', 'SURFACE'}:
            # For Curve objects, there can only be one material per spline
            #  and thus each spline is linked to one material slot.
            #  So to not have to care for different data structures for different curve types,
            #  we use the material slots and the built in selection methods
            #  (Technically, this should work for meshes as well)

            mat_slots = obj.material_slots

            i = 0
            for material in mat_slots:
                bpy.context.active_object.active_material_index = i

                if material.material == find_material:
                    bpy.ops.object.material_slot_select()
                    found_material = True
                elif not extend_selection:
                    bpy.ops.object.material_slot_deselect()

                i += 1

            if not found_material:
                self.report({'INFO'}, "Material " + find_material_name + " isn't assigned to slots!")

        else:
            # Some object types are not supported
            #  mostly because don't really support selecting by material (like Font/Text objects)
            #  ore that they don't support multiple materials/are just "weird" (i.e. Meta balls)
            self.report({'WARNING'}, "The type '" + obj.type + "' isn't supported in Edit mode by Material Utilities!")
            return {'CANCELLED'}

    return {'FINISHED'}


def mu_copy_material_to_others(self):
    """Copy the material to of the current object to the other seleceted all_objects"""
    # Currently uses the built-in method
    #  This could be extended to work in edit mode as well

    #active_object = context.active_object

    bpy.ops.object.material_slot_copy()

    return {'FINISHED'}


def mu_cleanmatslots(self):
    """Clean the material slots of the seleceted objects"""

    # check for edit mode
    edit_mode = False
    active_object = bpy.context.active_object
    if active_object.mode == 'EDIT':
        edit_mode = True
        bpy.ops.object.mode_set()

    objects = bpy.context.selected_editable_objects

    for obj in objects:
        used_mat_index = []  # we'll store used materials indices here
        assigned_materials = []
        material_list = []
        material_names = []

        materials = obj.material_slots.keys()

        if obj.type == 'MESH':
            # check the polygons on the mesh to build a list of used materials
            mesh = obj.data

            for poly in mesh.polygons:
                # get the material index for this face...
                material_index = poly.material_index

                if material_index >= len(materials):
                    poly.select = True
                    self.report({'ERROR'},
                                "A poly with an invalid material was found, this should not happen! Canceling!")
                    return {'CANCELLED'}

                # indices will be lost: Store face mat use by name
                current_mat = materials[material_index]
                assigned_materials.append(current_mat)

                # check if index is already listed as used or not
                found = False
                for mat in used_mat_index:
                    if mat == material_index:
                        found = True

                if not found:
                    # add this index to the list
                    used_mat_index.append(material_index)

            # re-assign the used materials to the mesh and leave out the unused
            for u in used_mat_index:
                material_list.append(materials[u])
                # we'll need a list of names to get the face indices...
                material_names.append(materials[u])

            mu_assign_material_slots(obj, material_list)

            # restore face indices:
            i = 0
            for poly in mesh.polygons:
                material_index = material_names.index(assigned_materials[i])
                poly.material_index = material_index
                i += 1

        elif obj.type in {'CURVE', 'SURFACE'}:

            splines = obj.data.splines

            for spline in splines:
                # Get the material index of this spline
                material_index = spline.material_index

                # indices will be last: Store material use by name
                current_mat = materials[material_index]
                assigned_materials.append(current_mat)

                # check if indek is already listed as used or not
                found = False
                for mat in used_mat_index:
                    if mat == material_index:
                        found = True

                if not found:
                    # add this index to the list
                    used_mat_index.append(material_index)

            # re-assigned the used materials to the curve and leave out the unused
            for u in used_mat_index:
                material_list.append(materials[u])
                # we'll need a list of names to get the face indices
                material_names.append(materials[u])

            mu_assign_material_slots(obj, material_list)

            # restore spline indices
            i = 0
            for spline in splines:
                material_index = material_names.index(assigned_materials[i])
                spline.material_index = material_index
                i += 1

        else:
            # Some object types are not supported
            self.report({'WARNING'},
                        "The type '" + obj.type + "' isn't currently supported " +
                        "for Material slots cleaning by Material Utilities!")

    if edit_mode:
        bpy.ops.object.mode_set(mode='EDIT')


def mu_remove_material(self, for_active_object = False):
    """Remove the active material slot from selected object(s)"""

    if for_active_object:
        bpy.ops.object.material_slot_remove()
    else:
        last_active = bpy.context.active_object
        objects = bpy.context.selected_editable_objects

        for obj in objects:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.material_slot_remove()

        bpy.context.view_layer.objects.active =  last_active

    return {'FINISHED'}

def mu_remove_all_materials(self, for_active_object = False):
    """Remove all material slots from selected object(s)"""

    if for_active_object:
        obj = bpy.context.active_object

        # Clear out the material slots
        obj.data.materials.clear()

    else:
        last_active = bpy.context.active_object
        objects = bpy.context.selected_editable_objects

        for obj in objects:
            obj.data.materials.clear()

        bpy.context.view_layer.objects.active = last_active

    return {'FINISHED'}


def mu_replace_material(material_a, material_b, all_objects=False, update_selection=False):
    """Replace one material with another material"""

    # material_a is the name of original material
    # material_b is the name of the material to replace it with
    # 'all' will replace throughout the blend file

    mat_org = bpy.data.materials.get(material_a)
    mat_rep = bpy.data.materials.get(material_b)

    if mat_org != mat_rep and None not in (mat_org, mat_rep):
        # Store active object
        scn = bpy.context.scene

        if all_objects:
            objs = bpy.data.objects
        else:
            objs = bpy.context.selected_editable_objects

        for obj in objs:
            if obj.type == 'MESH':
                match = False

                for mat in obj.material_slots:
                    if mat.material == mat_org:
                        mat.material = mat_rep

                        # Indicate which objects were affected
                        if update_selection:
                            obj.select_set(state = True)
                            match = True

                if update_selection and not match:
                    obj.select_set(state = False)

    return {'FINISHED'}


def mu_set_fake_user(self, fake_user, materials):
    """Set the fake user flag for the objects material"""

    if materials == 'ALL':
        mats = (mat for mat in bpy.data.materials if mat.library is None)
    elif materials == 'UNUSED':
        mats = (mat for mat in bpy.data.materials if mat.library is None and mat.users == 0)
    else:
        mats = []
        if materials == 'ACTIVE':
            objs = [bpy.context.active_object]
        elif materials == 'SELECTED':
            objs = bpy.context.selected_objects
        elif materials == 'SCENE':
            objs = bpy.context.scene.objects
        else: # materials == 'USED'
            objs = bpy.data.objects
            # Maybe check for users > 0 instead?

        mats = (mat for ob in objs if hasattr(ob.data, "materials") for mat in ob.data.materials if mat.library is None)

    if fake_user == 'TOGGLE':
        done_mats = []
        for mat in mats:
            if  not mat.name in done_mats:
                mat.use_fake_user = not mat.use_fake_user
            done_mats.append(mat.name)
    else:
        fake_user_val = fake_user == 'ON'
        for mat in mats:
            mat.use_fake_user = fake_user_val

    for area in bpy.context.screen.areas:
        if area.type in ('PROPERTIES', 'NODE_EDITOR'):
            area.tag_redraw()

    return {'FINISHED'}


def mu_change_material_link(self, link, affect, override_data_material = False):
    """Change what the materials are linked to (Object or Data), while keeping materials assigned"""

    objects = []

    if affect == "ACTIVE":
        objects = [bpy.context.active_object]
    elif affect == "SELECTED":
        objects = bpy.context.selected_objects
    elif affect == "SCENE":
        objects = bpy.context.scene.objects
    elif affect == "ALL":
        objects = bpy.data.objects

    for object in objects:
        for slot in object.material_slots:
            present_material = slot.material

            if link == 'TOGGLE':
                slot.link = ('DATA' if slot.link == 'OBJECT' else 'OBJECT')
            else:
                slot.link = link

            if slot.link == 'OBJECT' or override_data_material:
                slot.material = present_material

    return {'FINISHED'}
