
You can then hit the following endpoints:

| Method | Route      				| Body                                         						   |
| ------ | ------------------------ | -------------------------------------------------------------------- |
| GET    | /rate      				|                                              						   |
| GET    | /rate/exchange-list  	|                                              						   |
| POST   | /rate/insert-exchange    | `{"from": "currency 1", "to": "currency 2"}` 						   | 
| POST   | /rate/delete-exchange    | `{"from": "currency 1", "to": "currency 2"}` 						   | 
| POST   | /rate/insert-rate        | `{"from": "currency 1", "to": "currency 2", "rate": "float number"}` | 
