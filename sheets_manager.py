import os
import random
import string
import db
import json

FILENAME_LENGTH = 20

db = db.Database()


def generate_student_sheet(login):
    latex_template = "\documentclass{article} \n" \
                     "\\usepackage[T2A]{fontenc} \n" \
                     "\\usepackage[utf8]{inputenc} \n" \
                     "\\usepackage[russian]{babel} \n" \
                     "\\begin{document} \n" \
                     "\section*{Задачи} \n"

    query = "SELECT problems.tasks.statement FROM problems.cart " \
            "INNER JOIN problems.tasks ON problems.tasks.task_id = problems.cart.task_id " \
            "WHERE login=%s"
    params = [login,]
    db_response = json.loads(db.select_query(query, params))
    if db_response['code'] == 0:
        tasks_list = [i[0] for i in db_response['rows']]
        tasks_list = '\subsection{}' + '\n \n \subsection{}'.join(tasks_list)
        latex_template += tasks_list
        latex_template += "\n \end{document}"
        filename = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(FILENAME_LENGTH))
        fout = open('static/latex/' + filename + '.tex', 'w')
        print(latex_template, file=fout)
        fout.close()
        os.system('pdflatex -output-directory static/latex ' + filename + '.tex')
        return filename
    else:
        return None
