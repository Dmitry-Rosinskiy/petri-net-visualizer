from flask import Flask, render_template, redirect, request, flash, session, send_file

from visualizer import save_image
from filemanager import remove_extension, remove_file, remove_files, make_zip_archive

app = Flask(__name__)
# Секретный ключ приложения
app.secret_key = "47e082b0746d4fba0cf587c27897828a"

# Директория, где хранятся загружаемые файлы
upload_file_dir = "upload/files/"
# Директория, где хранятся изображения процессов
image_dir = "static/petri_net_images/"
# Название скачиваемого пользователем архива с изображениями процессов
archive_name = "petri_net_images.zip"

# Корневая страница (перенаправляет на страницу загрузки файлов)
@app.route("/")
def home():
    return redirect("/upload")

# Страница загрузки файлов
@app.route("/upload", methods=["GET", "POST"])
def upload():

    # Если метод запроса - POST (отправка формы)
    if request.method == "POST":

        # Успешная загрузка
        success_upload = True

        # Файл основного (иерархического) процесса
        process_file = request.files["process"]
        # Если файл основного (иерархического) процесса не был загружен пользователем
        if process_file.filename == "":
            # Создание сообщения пользователю
            flash("Не выбран файл основного процесса. Попробуйте снова.", category="warning")
            # Неудачная загрузка
            success_upload = False

        # Файлы подпроцессов
        subprocess_files = request.files.getlist("subprocesses")
        # Если файлы подпроцессов не были загружены пользователем
        if len(subprocess_files) > 0 and subprocess_files[0].filename == "":
            # Создание сообщения пользователю
            flash("Не выбраны файлы подпроцессов. Попробуйте снова.", category="warning")
            # Неудачная загрузка
            success_upload = False

        # Если загрузка неучдачная
        if not success_upload:
            # Показать страницу загрузки файлов
            return render_template("upload.html")  #img_url="https://upload.wikimedia.org/wikipedia/commons/f/fe/Detailed_petri_net.png")


        process_file.save(upload_file_dir + process_file.filename)
        # Если нельзя получить изображение основного (иерархического) процесса (формат файла неверный)
        if not save_image(upload_file_dir + process_file.filename, remove_extension(process_file.filename), image_dir):
            # Создание сообщения пользователю
            flash(f"Файл с основным процессом ({process_file.filename}) имеет неверный формат. Попробуйте снова.", category="error")
            # Неудачная загрузка
            success_upload = False

        correct_files = []
        incorrect_files = []
        for subprocess_file in subprocess_files:
            subprocess_file.save(upload_file_dir + subprocess_file.filename)
            # Если нельзя получить изображение подпроцесса (формат файла неверный)
            if not save_image(upload_file_dir +  subprocess_file.filename, remove_extension(subprocess_file.filename), image_dir):
                incorrect_files.append(subprocess_file.filename)
                # Неудачная загрузка
                success_upload = False
                continue
            correct_files.append(remove_extension(subprocess_file.filename))

        # Если загрузка неудачна
        if not success_upload:
            if len(incorrect_files) > 0:
                # Создание сообщения пользователю
                flash(f"Файл с подпроцессом ({', '.join(incorrect_files)}) имеет неверный формат. Попробуйте снова.", category="error")
                for incorrect_file in incorrect_files:
                    # Удаление некорректного файла подпроцесса
                    remove_file(upload_file_dir + incorrect_file)

            # Удаление файла основного (иерархического) процесса
            remove_file(upload_file_dir + process_file.filename)
            # Удаление изображения основного (иерархического) процесса
            remove_file(image_dir + remove_extension(process_file.filename) + ".png")
            for correct_file in correct_files:
                # Удаление корректных файлов подпроцессов
                remove_file(upload_file_dir + correct_file + ".pnml")
                # Удаление изображений подпроцессов
                remove_file(image_dir + correct_file + ".png")

            # Показать страницу загрузки файлов
            return render_template("upload.html")  #img_url="https://upload.wikimedia.org/wikipedia/commons/f/fe/Detailed_petri_net.png")

        # Сохранение в сессии названия основного (иерархического) процесса
        session["process"] = remove_extension(process_file.filename)
        # Сохранение в сессии названий подпроцессов
        session["subprocesses"] = correct_files

        # Перенаправить на страницу визуализации
        return redirect("/view")

    # Показать страницу загрузки файлов
    return render_template("upload.html")


# Страница визуализации
@app.route("/view", methods=["GET", "POST"])
def view():

    # Если метод запроса - GET (переход на страницу)
    if request.method == "GET":
        # Если файлы процессов были ранее загружены
        if "process" in session and "subprocesses" in session:
            # Показать страницу визуализации
            return render_template("view.html", process=session["process"], subprocesses=session["subprocesses"], image_dir=image_dir)
        else:
            # Создание сообщения пользователю
            flash("Чтобы запустить визуализацию, сначала выберите файлы.", category="warning")
            # Перенаправить на страницу загрузки файлов
            return redirect("/upload")

    # Если метод запроса - POST (пользователь возвращается на страницу загрузки файлов, нажав на кнопку возврата)
    if request.method == "POST":

        process_files = []
        # Если был загружен файл основного (иерархического) процесса
        if "process" in session:
            process_files.append(image_dir + session["process"] + ".png")
            process_files.append(upload_file_dir + session["process"] + ".pnml")
        # Если были загружены файлы подпроцессов
        if "subprocesses" in session:
            for subprocess in session["subprocesses"]:
                process_files.append(image_dir + subprocess + ".png")
                process_files.append(upload_file_dir + subprocess + ".pnml")
        # Удаление загруженных файлов процессов и их изображений
        remove_files(process_files)

        # Удаление информации о файлах из сессии
        session.pop("process", None)
        session.pop("subprocesses", None)

        # Перенаправить на страницу загрузки файлов
        return redirect("/upload")

# Страница скачивания архива
@app.route("/download")
def download():
    process_images = []
    # Если файлы процессов были ранее загружены
    if "process" in session and "subprocesses" in session:
        process_images.append(image_dir + session["process"] + ".png")
        for subprocess in session["subprocesses"]:
            process_images.append(image_dir + subprocess + ".png")

        # Создание архива с изображениями и его скачивание из браузера
        return send_file(make_zip_archive(process_images), as_attachment=True, download_name=archive_name)

    else:
        # Создание сообщения пользователю
        flash("Чтобы скачать файлы, сначала выберите файлы и запустите визуализацию.", category="warning")
        # Перенаправить на страницу загрузки
        return redirect("/upload")


# Запуск приложения
if __name__ == "__main__":
    app.run(debug=True)
