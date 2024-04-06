import pm4py

# Сохранение изображения сети Петри, заданной с помощью файла .pnml
def save_image(pnml_file, file_name, directory, data):
    data.clear()
    try:
        # Создание модели сети Петри на основании файла
        net, initial_marking, final_marking = pm4py.read_pnml(pnml_file)
        print(net.properties)
        for transition in net.transitions:
            label = transition.properties.get("trans_name_tag")
            graphics = transition.properties.get("layout_information_petri")
            if label is not None and graphics is not None:
                coords = {"x":graphics[0][0], "y":graphics[0][1]}
                data.setdefault(label, coords)

        # Конвертирование модели в изображение формата .png
        pm4py.save_vis_petri_net(net, initial_marking, final_marking,  directory + file_name + ".png", debug=False)
    except Exception:
        # Неудачное сохранение
        return False

    # Удачное сохранение
    return True
