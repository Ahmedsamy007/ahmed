def alarm_filter(txt):
    import re
    text = '{}{}{}'.format(' ', txt, ' ')
    day = 0
    regect = False
    action = ''
    hour = ''
    minute = ''
    indicator = ''
    Am_Pm = ''
    try:
        if re.search(r"بعد |كمان |غفوه ", text):

            info = re.search(r".* (بعد|كمان|غفوه) (\w+) ((ساعه|ساعات) )?((و|الا ) ?(\w+))? ?.*", text)
            if not re.search(r"ساعه | ساعات |ساعتين ", text):
                hour = 0
                minute = info.group(2)

            else:
                hour = info.group(2)

                minute = info.group(7)

                indicator = info.group(6)

            m_hour = {('ساعة', 'ساعه'): '1', ('ساعتين', 'ساعتين'): '2', ('ثلاث', 'ثلاثه', 'ثلاثة'): '3',
                      ('اربع', 'اربعه'): '4',
                      ('خمس', 'خمسه'): '5', ('ست', 'سته'): '6', ('سبع', 'سبعه'): '7'
                , ('ثمان', 'ثمن'): '8', ('تسع', 'تسعه'): '', ('عشر', 'عشره'): '10', ('نص', 'نصف'): '.5',
                      ('ربع',): '.25', ('تلت', 'ثلث'): '1/3'}
            m_minute = {('دقيقه', 'دقيقة'): '1', ('دقيقتين',): '2', ('ثلاثه', 'ثلاث'): '3', ('اربع', 'اربعه'): '4',
                        ('ست', 'سته'): '6'
                , ('سبع', 'سبعه'): '2', ('ثمان', 'ثمن'): '8', ('تسع', 'تسعه'): '2', ('نص', 'نصف'): '30', ('ربع',): '15',
                        ('تلت', 'ثلث'): '1/3', ('خمسه', 'خمسة', 'خمس'): '5', ('عشرة', 'عشره'): '10', (None,): '0'}
            Real_hour = hour
            Real_minute = minute
            for keys, val in m_hour.items():
                for key in keys:
                    if key == hour:
                        Real_hour = val
                        regect = True
                        break
                if regect:
                    break
            regect = False
            for keys, val in m_minute.items():
                for key in keys:
                    if key == minute:
                        Real_minute = val
                        regect = True
                        break
                if regect:
                    break

            time = (int(Real_hour) * 60 + int(Real_minute)) * 60
            if indicator == 'الا ':
                time = (int(Real_hour) * 60 - int(Real_minute)) * 60

            action = 'set'
            All_info = {'time': time, 'day': 0, 'action': action}
            return All_info



        else:

            if re.search(r"اصحي|صحيني|رن|منبه|قومني|شغل", text):
                if re.search(r".* (بكره|منبه|الساعه|صحيني|اصحي|قومني) ?(\w+) ((و|الا ) ?(\w+))? ?.*", text):

                    result = re.search(r".* (بكره|منبه|الساعه|صحيني|اصحي|قومني) ?(\w+) ((و|الا ) ?(\w+))? ?.*", text)
                    hour = result.group(2)
                    print ( 'hour=' , hour )
                    indicator = result.group(4)
                    # print ( 'indicator =' , indicator )
                    minute = result.group(5)
                    # print ( 'minutes = ' , minute )

                    if re.search(r"بكره|بكرة", text):
                        day = 1

                    if re.search(r"الصبح|صباحا", text):
                        Am_Pm = 'AM'
                    if 'بعد بكره' in text:
                        day = 2
                    # print ( 'day = ' , day )

                    if re.search(r'مساءا|بالليل', text):
                        Am_Pm = 'PM'

            if re.search(r"اصحي|صحيني|رن|منبه|قومني|شغل", text):
                action = 'set'
                # print ( 'action = ' , action )
            if re.search(r'الغاء|الغي|امسح', text):
                action = 'cancel'
                # print ( 'action = ' , action )

            matching_hour = {('واحده', '1'): '01', ('اثنين', '2'): '02', ('ثلاثه', '3'): '03', ('اربعه', '4'): '04',
                             ('خمسه', '5'): '05', ('سته', '6'): '06'
                , ('سبعه', '7'): '07', ('ثمانيه', '8'): '08', ('تسعه', '9'): '09', ('عشره', '10'): '10',
                             ('11', '11.'): '11', ('12', '12.'): '12', (None,): '00'}

            matching_min = {('خمسه', 'خمس'): '05', ('عشره', 'عشر'): '10', ('ربع', '15'): '15', ('تلت', 'ثلث'): '20',
                            ('نص', 'نصف'): '30', (None,): '00'}

            Real_hour = hour
            Real_minute = minute

            for keys, val in matching_hour.items():
                for key in keys:
                    if key == hour:
                        Real_hour = val
                        regect = True
                        break
                if regect:
                    break
            regect = False
            for keys, val in matching_min.items():
                for key in keys:
                    if key == minute:
                        Real_minute = val
                        regect = True
                        break
                if regect:
                    break

            if indicator == 'الا ':
                Real_hour = int(Real_hour) - 1
                Real_minute = 60 - int(Real_minute)

            # print ( 'real hour = ' , Real_hour )
            # print ( 'real minute = ' , Real_minute )
            # print ( 'real room = ' , Real_room )
            time = '{}:{}:00 {}'.format(Real_hour, Real_minute, Am_Pm)
            # print ( 'time = ' , time )

            All_info = {'day': day, 'time': time, 'action': action}
            # print ( All_info )

            if time == '::00 ' and action != 'cancel':
                return False

            elif time == '::00 ' and action == 'cancel' :
                return {'time': None, 'action': 'cancel'}



            else:
                return All_info






    except AttributeError:
        print('Please try To Say It In a Suitable Format')


