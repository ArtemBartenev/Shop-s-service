# Shop-s-service description
### Using this module you can interact with shop's showcase. 
### You be able to add companies, employees, goods and appoint employees for the goods.
#### Example 1.
At first, you need create instance of `ShowcaseService` class from module `methods`. Passing as argument `URL`. Then you call
 instance method `add_company()`, and finally call method `execute()`.
```python 
service = ShowcaseService(URL)
service.add_company("Orange", "New-York", "mandarin@orange.com", "555-55-55")
service.execute()
```
##### notice:
If you call `execute()` without calling methods `add_company`,
`add_good` e.g. before, it will raise `ServiceExecuteError`.

#### Example 2.
Before `execute()` you can call more than one method.
```python
service = ShowcaseService(URL)
service.add_company("Orange", "New-York", "mandarin@orange.com", "555-55-55")
service.add_company("IMB", "CA, "damnbigcompany@ibm.com", "999-99-99")
service.add_company("Pear", "La", "Pearphone@pear.com", "111-11-00")
service.execute()
```
##### explanation:
When you call method `add_company`, `add_employee`, `add_good`, `appoint_employee` you only register coro for further requests. 
