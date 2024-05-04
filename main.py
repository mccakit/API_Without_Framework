from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import random

with open('menu.json', 'r') as file:
    menu = json.load(file)


class NeuralHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if parsed_path.path == "/listMeals":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(menu["meals"], indent=4), "utf-8"))
        elif parsed_path.path == "/getMeal":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            meal = [item for item in menu["meals"] if item["id"] == int(query_params["id"][0])]
            self.wfile.write(bytes(json.dumps(meal, indent=4), "utf-8"))


    def do_POST(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if parsed_path.path == "/quality":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            meal_ingredients = [item["ingredients"] for item in menu["meals"] if
                                item["id"] == int(query_params["meal_id"][0])]
            meal_ingredient_names = [str(ingredient["name"]).lower() for ingredient in meal_ingredients[0]]
            tierlist = {"high": 3, "medium": 2, "low": 1}
            score = 0
            for ingredient in meal_ingredient_names:
                print(ingredient)
                if ingredient in query_params.keys():
                    score += tierlist[query_params[ingredient][0]]
                else:
                    score += tierlist["high"]
            self.wfile.write(bytes(json.dumps({"quality": score}, indent=4), "utf-8"))
        elif parsed_path.path == "/price":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            meal = [item for item in menu["meals"] if item["id"] == int(query_params["meal_id"][0])]
            meal_ingredients = [item["ingredients"] for item in menu["meals"] if
                                item["id"] == int(query_params["meal_id"][0])]
            meal_ingredient_names = [str(ingredient["name"]).lower() for ingredient in meal_ingredients[0]]
            ingredients = [ingredient for ingredient in menu["ingredients"] if
                           str(ingredient["name"]).lower() in meal_ingredient_names]
            filtered_ingredients = []
            for ingredient in ingredients:
                if str(ingredient["name"]).lower() in query_params.keys():
                    for option in ingredient["options"]:
                        if option["quality"] == query_params[str(ingredient["name"]).lower()][0]:
                            option["name"] = str(ingredient["name"]).lower()
                            filtered_ingredients.append(option)
                else:
                    for option in ingredient["options"]:
                        if option["quality"] == "high":
                            option["name"] = str(ingredient["name"]).lower()
                            filtered_ingredients.append(option)
            for ingredient in meal_ingredients[0]:
                if ingredient["quantity_type"] in ["millilitre", "gram"]:
                    ingredient["quantity"] = ingredient["quantity"] / 1000
            price = 0
            for ingredient_quantity in meal_ingredients[0]:
                for ingredient_value in filtered_ingredients:
                    if str(ingredient_quantity["name"]).lower() == ingredient_value["name"]:
                        price += ingredient_quantity["quantity"] * ingredient_value["price"]
            price = round(price, 2)

            self.wfile.write(bytes(json.dumps({"price": price}), "utf-8"))
        elif parsed_path.path == "/random":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            quality_list = ["high", "low", "medium"]
            meal = random.choice(menu["meals"])
            for i in range(len(meal["ingredients"])):
                meal["ingredients"][i] = {"name": meal["ingredients"][i]["name"],
                                          "quality": random.choice(quality_list)}

            self.wfile.write(bytes(json.dumps(meal, indent=4), "utf-8"))


server = HTTPServer(("localhost", 8000), NeuralHTTP)
server.serve_forever()
server.server_close()
