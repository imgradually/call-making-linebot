Help_message_for_admin = '''下SQL指令:SQL {SQL_order}
ex:
1. UPDATE table_name SET col1 = 'val1' WHERE col2 = 'val2'

2. INSERT INTO table_name (col1,col2) VALUES (val1,val2)

3. DELETE FROM table_name WHERE col = 'val'

顯示: show {內容}
(你的ID)show pid
(群組ID)show gid
(用戶們)show users
(群組們)show groups

新增:   add {類型} {內容}
(使用者)add user {名稱} {電話}
( 團隊 )add group {名稱} {IT/CC}
( 管理員 )add admin {名稱}

刪除:  delete {類型} {名稱}
(使用者)delete user {名稱}
( 群組 )delete group {名稱}

查詢用戶電話:search user {名稱}
重複:Echo {內容}
打招呼:Hi / Hello
換招呼:Change {新招呼}

打電話:Call {使用者名稱}'''

Help_message = '''
新增你的資料:add user {名稱} {電話}
刪除你的資料:Delete myself
'''
Help_in_a_group = "請私訊linebot"