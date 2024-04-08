from pm4py import read_pnml, save_vis_petri_net

# from pm4py.objects.petri_net.importer import importer as petri_importer

# Сохранение изображения сети Петри, заданной с помощью файла .pnml
def save_image(pnml_file, file_name, directory, data):
    data.clear()
    try:
        # Создание модели сети Петри на основании файла
        net, initial_marking, final_marking = read_pnml(pnml_file)
        # net, initial_marking, final_marking = pm4py.objects.petri_net.importer.variants.pnml.import_net(pnml_file)
        for transition in net.transitions:
            label = transition.properties.get("trans_name_tag")
            graphics = transition.properties.get("layout_information_petri")
            if label is not None and graphics is not None:
                coords = {"x": graphics[0][0], "y": graphics[0][1]}
                data.setdefault(label, coords)

        # Конвертирование модели в изображение формата .png
        save_vis_petri_net(net, initial_marking, final_marking, directory + file_name + ".png")
    except Exception as e:
        print(e)
        # Неудачное сохранение
        return False

    # Удачное сохранение
    return True
