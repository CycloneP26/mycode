#!/usr/bin/env python3

import json
import locale
import sys
import reports
import emails
import os

def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
  max_revenue = {"revenue": 0}
  best_car = {}
  best_year = {}
  bestest_year = ()
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    # TODO: also handle max sales
    if item == data[0]:
      best_car = item
    if item["total_sales"] > best_car["total_sales"]:
      best_car = item
    # TODO: also handle most popular car_year
    if item["car"]["car_year"] in best_year:
      best_year[item["car"]["car_year"]] += item["total_sales"]
    else:
      best_year[item["car"]["car_year"]] = item["total_sales"]
  print(best_year)
  srt_yrs = sorted(best_year.items(), key = lambda x: x[1], reverse=True)
  print(srt_yrs)
  bestest_year = srt_yrs[0]
  print("bst_yr = " + str(bestest_year))
  summary = [
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]),
    "The {} had the most sales: {}".format(
      best_car["car"]["car_model"], best_car["total_sales"]),
    "The most popular year was {} with {} sales.".format(
      bestest_year[0], bestest_year[1])
  ]
  return summary


def cars_dict_to_table(car_data):
#  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data


def main(argv):
#  """Process the JSON data and generate a full report out of it."""
  data = load_data("car_sales.json")
  summary = process_data(data)
  table_data = cars_dict_to_table(data)
  print(summary)
  # TODO: turn this into a PDF report
  reports.generate("/tmp/cars.pdf", "Sales summary for last month", summary[0] + "<br/>" + summary[1] + "<br/>" + summary[2], table_data)
  # TODO: send the PDF report as an email attachment
  sender = "automation@example.com"
  receiver = "{}@example.com".format(os.environ.get('USER'))
  subject = "Sales summary for last month"
  body = "{}\n{}\n{}".format(summary[0], summary[1], summary[2])
  message = emails.generate(sender, receiver, subject, body, "/tmp/cars.pdf")
  emails.send(message)



if __name__ == "__main__":
  main(sys.argv)
