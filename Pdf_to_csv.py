import fitz
import re
import traceback
import pandas as pd


def pdf_to_csv(filename):

    text = ''
    main_task_order = 1

    # fullpath = f'requests\{filename}'
    fullpath = filename 
    with fitz.open(fullpath) as doc:
        for page in doc:
            # считаем количество страниц и объединяем все страницы в одну string переменную
            text = text + (page.get_text())

    while True:
        wrong_flag = False
        task_order = 1
        index_start_main_task = text.find(f'Подзапрос №{main_task_order}')
        index_end_main_task = text.find(f'Подзапрос №{main_task_order + 1}')
        
        # Если не находим Подзапрос, то break
        if index_start_main_task == -1:
                break
        
        while True:
            try:
                task_list = []
                # Находим индексы начала и конца Задания №n
                number_of_task = f'Заказ №{task_order}'
                next_number_of_task = f'Заказ №{task_order + 1}'
                
                if index_end_main_task == -1:
                    index_start_task = text.find(number_of_task, index_start_main_task)
                    index_end_task = text.find(next_number_of_task, index_start_main_task)
                else:
                    index_start_task = text.find(number_of_task, index_start_main_task, index_end_main_task)
                    index_end_task = text.find(next_number_of_task, index_start_main_task, index_end_main_task)   
                # Если Заказ №n не найден (выдаст индекс -1), то выход из цикла
                if index_start_task == -1:
                    break
                # Проверка для последней задачи в подзапросе
                if index_end_task == -1 and index_end_main_task == -1:
                    index_end_task = 100000000000000000000000000
                elif index_end_task == -1 and index_end_main_task != -1:
                    index_end_task = index_end_main_task - 2
                else:
                    index_end_task = index_end_task 

                # print(f'Ищу текст между координатами {index_start_task} и {index_end_task}')
                # # Выводим текущее найденное Задание №n 
                print(f'{text[index_start_task:index_start_task + 10]}')
                print('...')
                
                # Задаём регулярные выражения на поиски строк
                pattern_time_start = r"(Время подачи:)\s+(\d{2}.\d{2}.\d{4}\s+\d{2}:\d{2}:\d{2})"
                pattern_points = r'([А-Я].+?)\s\|'
                pattern_abonent_number = r"(Телефон пассажира:)\s+((\+7|8)\d{10})"
                pattern_from_destination = r'(Откуда:)\s(.+?)\|'
                pattern_to_destination = r'(Куда:)\s(.+?)\|'
                pattern_complete = r'(Заказ выполнен:)\s(да|нет)'

                # Ищем cтроки регулярками
                abonent_time_start = re.search(pattern_time_start, text[index_start_task : index_end_task])                

                # Находим индекс начала и конца Промежуточных точек для ограничения
                index_points_start = text.find('Промежуточные точки:', index_start_task, index_end_task)
                index_points_end = text.find('Телефон пассажира:', index_start_task, index_end_task)

                # Проверка на валидность ОТКУДА и КУДА, иначе в df записывается меньше строк, чем надо и ошибка
                if re.search(pattern_from_destination, text[index_start_task : index_end_task].replace('\n', ' ').replace('- ', '')) is not None:
                    abonent_from_destination = re.finditer(pattern_from_destination, text[index_start_task : index_end_task].replace('\n', ' ').replace('- ', ''))
                else:
                    abonent_from_destination = '-'

                if re.search(pattern_to_destination, text[index_start_task : index_end_task].replace('\n', ' ').replace('- ', '')) is not None: 
                    abonent_to_destination = re.finditer(pattern_to_destination, text[index_start_task : index_end_task].replace('\n', ' ').replace('- ', ''))  
                else:
                    abonent_to_destination = '-'    
             
                abonent_number =re.search(pattern_abonent_number, text[index_start_task : index_end_task])

                abonent_complete = re.search(pattern_complete, text[index_start_task : index_end_task], flags=re.IGNORECASE)
                    

                # # Принтим для проверки и добавляем в список
                task_list.append(task_order)

                try:
                    if abonent_complete == None or abonent_complete.group(2).upper() == 'ДА':
                        task_list.append(abonent_time_start.group(2))
                        print(abonent_time_start.group(2)) 
                    else:
                        task_list.append(abonent_time_start.group(2) + ' ' + '(Заказ не выполнен)') 
                        print(abonent_time_start.group(2) + ' ' + '(Заказ не выполнен)')      
                except:    
                    task_list.append(abonent_time_start.group(2))    
                    print(abonent_time_start.group(2))  

                if abonent_from_destination != '-':
                    for i in abonent_from_destination:
                        print(i.group(2))
                        task_list.append(i.group(2))
                else:
                    print('-')
                    task_list.append('-')        
                
                if abonent_to_destination != '-':
                    for i in abonent_to_destination:
                        print(i.group(2))
                        task_list.append(i.group(2))   
                else:
                    print('-')
                    task_list.append('-')        

                if index_points_start != -1:
                    points = re.finditer(pattern_points, text[index_points_start + 20 : index_points_end].replace('\n', ' ').replace('- ', ''))
                    if points != None:
                        points_list = []
                        # Подумай, как засунуть сразу 2 запроса
                        for i in points:
                            print(i.group(1))
                            points_list.append(i.group(1))
                        if len(points_list) > 1:
                            temp_string = ', '.join(points_list)
                            task_list.append(temp_string)
                        else:
                            task_list.append(points_list[0])       
                else:
                    points = ' '
                    print('-')
                    task_list.append(points)

                print(abonent_number.group(2) if abonent_number else '-') 
                if abonent_number != None:
                    task_list.append(abonent_number.group(2))
                else:
                    task_list.append('-')    

                # Фомируем data frame 
                if task_order == 1:
                    df = pd.DataFrame([task_list], columns=['№ п/п', 'Дата и время отправления', 'Место отправления', 'Место назначения', 'Промежуточные точки', 'Номер абонента'])  
                else:
                    df.loc[len(df.index)] = task_list  

                # Повышаем номер Задания №n
                task_order += 1       
            except Exception as e:
                print('Ошибка:\n', traceback.format_exc())
                print(f'Закончил на {task_order - 1} заказе')
                break  
        
        # Формируем excel-файл xlsx
        try:
            pattern = r'\d+\.pdf'
            xlsx_name = f'requests\{ re.search(pattern, filename).group(0) }-Подзадача-{main_task_order}.xlsx'
            df.to_excel(xlsx_name, index=False)
        except Exception as e:
            wrong_flag = True
            print('Произошла ошибка, возможно, отчетный файл или подзадача безрезультативный')  
            print(e) 

        if not wrong_flag:
            print(f'Успешно обработано {task_order - 1} задач в {main_task_order} подзадаче')       
        
        main_task_order += 1         
    
    