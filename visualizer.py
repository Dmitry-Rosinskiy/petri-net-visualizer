import pm4py

# Сохранение изображения сети Петри, заданной с помощью файла .pnml
def save_image(pnml_file, file_name, directory):
    try:
        # Создание модели сети Петри на основании файла
        net, initial_marking, final_marking = pm4py.read_pnml(pnml_file)
        # Конвертирование модели в изображение формата .png
        pm4py.save_vis_petri_net(net, initial_marking, final_marking,  directory + file_name + ".png")
    except Exception:
        # Неудачное сохранение
        return False

    # Удачное сохранение
    return True
