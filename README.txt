процесс работы:

предметная область:
"18. Выдача банком кредитов
Описание предметной области
Вы являетесь руководителем информационно-аналитического центра коммерческого банка.
Одним из существенных видов деятельности банка является выдача кредитов юридическим лицам. 
Вашей задачей является отслеживание динамики работы кредитного отдела. 
В зависимости от условий получения кредита, процентной ставки и срока возврата все кредитные операции делятся на несколько основных видов. 
Каждый из этих видов имеет свое название. 
Кредит может получить клиент, при регистрации предоставивший следующие сведения: название, вид собственности, адрес, телефон, контактное лицо. 
Каждый факт выдачи кредита регистрируется банком, при этом фиксируются сумма кредита, клиент и дата выдачи."

явного тз не дано, как и того, к чему мы должны прийти в конце или хотя бы приблизиться на последних итерациях проекта, ни mvp, ничего.
по этому я сам решил для себя поставить цель и постараться к ней приблизиться.

как я вижу итог: сайт, с системой регистрации/авторизации,
а так же система для подачи заявки на получения кредита/раннего получения результата анализа кредитования
(финальное решение о выдаче кредита принимает менеджер, а модель выдает лишь ожидаемый ответ да/нет = вероятно/менее вероятно).

получается так:
backend(fastapi) + db(postgreSQL/alembic) + ml(logistic regression) + frontend(базовый html/css/js) + обернуть в docker + поставить на хостинг
все идет в порядке важности и необходимости.