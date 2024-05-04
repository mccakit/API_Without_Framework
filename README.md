This is a API written in Python using only the built in libraries.
It has 2 get methods and 3 post methods:

-Get Methods

-	/listMeals

	Lists all the meals in the dataset in json format
-	/getMeal, params = id<int>


	Lists a meal that shares the id number of the parameter
-POST Methods

- 	/quality params = id<int>,<ingredient><string>,...

  	Returns the average quality of the ingredients of a meal that shares the id number of the parameter
  	if no quality parameter is given, it is assumed the ingredient has the highest quality

-	/price	params = id<int>,<ingredient><string>,...

  	Returns the total ingredient cost of a meal that shares the id number of the parameter.

- 	/random

  	Lists a meal with randomized ingredient qualities.
