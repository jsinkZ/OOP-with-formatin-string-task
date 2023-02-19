# OOP simple with formating strings, try except construct and calls counter

## Update history

##### Created method for class Company: `.send_corporate_email`

- After call will send message for only worker else fail
- If success will printed else printed error
- Recipient will get this message
- `<Company>.send_corporate_email(Worker, message)`

##### Created private method for class Worker: `._get_message`

- Showing in console message from sent company
- `<Worker>._get_message(Company, message)`

##### Created decorator `@count_calls`

- After connect to function, decorator will count calls in global dict (calls_counter storage)
- To get all calls `print(calls_counter)`
