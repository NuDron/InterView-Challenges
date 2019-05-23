import os, datetime, csv
from datetime import datetime
from datetime import timedelta

"""
Please write you name here: KRZYSZTOF SZUMKO
This file was submitted on 22-May-2019
"""


def process_shifts(path_to_csv):
    """

    :param path_to_csv: The path to the work_shift.csv
    :type string:
    :return: A dictionary with time as key (string) with format %H:%M
        (e.g. "18:00") and cost as value (Number)
    For example, it should be something like :
    {
        "17:00": 50,
        "22:00: 40,
    }
    In other words, for the hour beginning at 17:00, labour cost was
    50 pounds
    :rtype dict:
    """
    # Empty Dictionary for storing data from wrok_shifts *.csv file.
    dataFromWorkShifts = {}

    # Reading the file and filling dataFromWorkShifts.
    with open(path_to_csv, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        counter = 0
        for row in spamreader:
            dataFromWorkShifts[counter] = row
            counter += 1
    # Get rid of unnecessary strings in data.
    dataFromWorkShifts.pop(0)
    employee = {}
    # Earliest time from all of the employees.
    earliestTimeEver = ""
    # Latest time from all of the employees.
    latestTimeEver = ""

    for key, val in dataFromWorkShifts.items():
        newTime = datetime.strptime(val[3], '%H:%M')
        newTime2 = datetime.strptime(val[1], '%H:%M')
        hourRate = val[2]
        if earliestTimeEver == "":
            earliestTimeEver = newTime
        if newTime < earliestTimeEver:
            earliestTimeEver = newTime
        if latestTimeEver == "":
            latestTimeEver = newTime2
        if newTime > latestTimeEver:
            latestTimeEver = newTime2
        tempVal = str(val[0])
        startOfBreak = getStartOfBreakTime(tempVal)
        finishOfBreak = getFinishOfBreakTime(tempVal)
        # Create a data (in 10 min increments) to hold all of the emplyees break times.
        allEmployeeBreak = createHoursBetween(startOfBreak, finishOfBreak)

        # Create dictionary of redefined employee objects.
        employee[key] = {'breakTime': allEmployeeBreak, 'latestHour': newTime2, 'hourRate': hourRate,
                         'firstHour': newTime}

    # Creation of simple time table (using datetime type) from earliest hours worked to latest.
    entireDay = createHoursBetween(earliestTimeEver, latestTimeEver)
    # Method generateTimetable produces a final result of dictionary object with hours (as key)
    # and labour cost (as value).
    result = generateTimetable(entireDay, earliestTimeEver, latestTimeEver, employee)
    return result


def generateTimetable(aTimetable, startTime, finishTime, anEmployee):
    result = {}
    allEmployeeHours = {}
    allEmployeeHoursWithoutBreaks = {}
    # Creating a full hours schedule (in 10 min increments) for each individual employee.
    for eachOne in anEmployee:
        tempFirstHour = anEmployee[eachOne]
        tempFirstHour = tempFirstHour['firstHour']
        tempLastHour = anEmployee[eachOne]
        tempLastHour = tempLastHour['latestHour']
        tempHours = createHoursBetween(tempFirstHour, tempLastHour)
        allEmployeeHours[eachOne] = tempHours

    # Creating a variable holding all of the individual employees hours trimmed from break times.
    for eachOne in anEmployee:
        all_hours = allEmployeeHours[eachOne]
        all_breaks = anEmployee[eachOne]
        all_breaks = all_breaks['breakTime']
        all_breaks = all_breaks[1:-1]
        for i in all_breaks:
            if i in all_hours:
                all_hours.remove(i)
        allEmployeeHoursWithoutBreaks[eachOne] = all_hours
    plain_timetable = createPlainHours(startTime, finishTime)
    for i in aTimetable:
        labour_cost = 0
        for eachSingle in anEmployee:
            hour = allEmployeeHoursWithoutBreaks[eachSingle]
            if i in hour:
                payRate = anEmployee[eachSingle]
                payRate = float(payRate['hourRate']) / 6
                labour_cost = labour_cost + payRate
        result[i] = labour_cost
    labour_cost = {}
    for hour in plain_timetable:
        temp = str(hour).split(":")
        temp = temp[0]
        tempInt = 0
        for key in result:
            temp2 = str(key).split(":")
            temp2 = temp2[0]
            if temp == temp2:
                tempInt = tempInt + result[key]
        formattedTime = temp + ":00"
        labour_cost[formattedTime] = int(round(tempInt))
    finalResult = labour_cost
    del finalResult['23:00']
    return finalResult


def getStartOfBreakTime(aString):
    if aString.find("PM"):
        aString = str(aString).replace("PM", "")
    aString = str((aString.split("-"))[0])
    aString = aString.strip()
    if len(aString) == 2:
        aString = aString + ":00"
        breakStart = datetime.strptime(aString, '%H:%M')
        return breakStart
    if len(aString) == 1:
        aString = changeFrom12To24(aString)
        aString = aString + ":00"
        breakStart = datetime.strptime(aString, '%H:%M')
        return breakStart
    if aString.find("."):
        aString = aString.replace(".", ":")
        breakStart = datetime.strptime(aString, '%H:%M')
        return breakStart
    return aString

def createHoursBetween(startTime, finishTime):
    """
    Creates a list of datetime object filling the gap between supplied startTime and finishTime.
    :param startTime: datetime object
    :param finishTime: datetime object
    :return: a List of datetime objects incremented by 10 min.
    """
    result = []
    difference = finishTime - startTime
    difference = str(difference).split(":")
    difference = int(difference[0]) + (int(difference[1]) / 60)
    difference = difference * 6
    for i in range(int(difference)):
        if startTime < finishTime:
            temp = startTime.time()
            result.append(temp)
            startTime = startTime + timedelta(minutes=10)
        if startTime == finishTime:
            temp = finishTime.time()
            result.append(temp)
    return result


def createPlainHours(startTime, finishTime):
    """
        Creates a list of datetime object filling the gap between supplied startTime and finishTime.
        :param startTime: datetime object
        :param finishTime: datetime object
        :return: a List of datetime objects incremented by 60 min.
    """
    result = []
    difference = finishTime - startTime
    difference = str(difference).split(":")
    difference = int(difference[0]) + (int(difference[1]) / 60)
    for i in range(int(difference)):
        if startTime < finishTime:
            temp = startTime.time()
            result.append(temp)
            startTime = startTime + timedelta(minutes=60)
        if startTime == finishTime:
            temp = finishTime.time()
            result.append(temp)
    return result


def getFinishOfBreakTime(aString):
    """
    Sanitises the hour aString provided and makes it into a standardised DateTime object.
    :param aString:
    :return:
    """
    if aString.find("PM"):
        aString = str(aString).replace("PM", "")
    aString = str((aString.split("-"))[1])
    aString = aString.strip()
    if len(aString) == 2:
        aString = aString + ":00"
        breakStart = datetime.strptime(aString, '%H:%M')
        return breakStart
    if len(aString) == 1:
        aString = changeFrom12To24(aString)
        aString = aString + ":00"
        breakStart = datetime.strptime(aString, '%H:%M')
        return breakStart
    if aString.find("."):
        aString = aString.replace(".", ":")
        if len(aString) == 4:
            temp = aString.split(":")
            aString = changeFrom12To24(str(temp[0])) + ":" + str(temp[1])
        breakStart = datetime.strptime(aString, '%H:%M')
        return breakStart
    return aString


def changeFrom12To24(aString):
    """
    Changes the format from am/pm to 24h system.
    :param aString: String representing an hour value.
    :return:
    """
    if aString == "1":
        aString = "13"
    if aString == "2":
        aString = "14"
    if aString == "3":
        aString = "15"
    if aString == "4":
        aString = "16"
    if aString == "5":
        aString = "17"
    if aString == "6":
        aString = "18"
    if aString == "7":
        aString = "19"
    if aString == "8":
        aString = "20"
    if aString == "9":
        aString = "21"
    if aString == "10":
        aString = "22"
    if aString == "11":
        aString = "23"
    return aString


def process_sales(path_to_csv):
    """

    :param path_to_csv: The path to the transactions.csv
    :type string:
    :return: A dictionary with time (string) with format %H:%M as key and
    sales as value (string),
    and corresponding value with format %H:%M (e.g. "18:00"),
    and type float)
    For example, it should be something like :
    {
        "17:00": 250,
        "22:00": 0,
    },
    This means, for the hour beginning at 17:00, the sales were 250 dollars
    and for the hour beginning at 22:00, the sales were 0.

    :rtype dict:
    """
    oldRow = ""
    dataFromTransactions = {}
    result = {}
    with open(path_to_csv, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:

            # There are double time values in provided dataset. Dictionary double keys are automatically overwritten.
            if row[1] not in dataFromTransactions.keys():
                dataFromTransactions[row[1]] = row[0]
            else:
                try:
                    dataFromTransactions[row[1]] = float(row[0]) + oldRow
                except:
                    dataFromTransactions[row[1]] = 0
            try:
                oldRow = float(row[0])
            except:
                oldRow = 0


    # Delete unnecessery dataset decsription items.
    del dataFromTransactions['time']
    firstItem = list(dataFromTransactions.items())[0]
    lastItem = list(dataFromTransactions.items())[-1]
    firstItem = standarizeHour(firstItem[0])
    lastItem = standarizeHour(lastItem[0])
    plainTimeTable = createPlainHours(firstItem, lastItem)
    standarisedPlainTable = []
    for x in plainTimeTable:
        temp = str(x).split(":")
        temp = temp[0] + ":" + temp[1]
        standarisedPlainTable.append(temp)
    for x in standarisedPlainTable:
        result[x] = 0

    for x in dataFromTransactions:
        currentHr = standarizeHour(x)
        currentHr = stringifyHour(currentHr)
        val = dataFromTransactions[x]
        tempInt = result[currentHr]
        result[currentHr] = round(tempInt + float(val), 2)
    return result


def generateSale(aTable, currentHr, aFloat):
    tempInt = 0

    for y in aTable:
        if y == currentHr:
            tempInt = tempInt + aFloat
        if y > currentHr:
            return tempInt


def stringifyHour(anHour):
    """
    Takes object of datetime type and makes a short string of HOUR only.
    In HH:MM format.
    :param anHour: an object of datetime type
    :return:
    """
    result = str(anHour).split(" ")
    result = result[1]
    result = str(result).split(":")
    result = str(result[0]) + ":" + str(result[1])
    return result


def standarizeHour(aString):
    if aString.find(":"):
        aString = aString.split(':')
        aString = aString[0]
    aString = aString + ":00"
    aString = datetime.strptime(aString, '%H:%M')
    return aString


def compute_percentage(shifts, sales):
    """
    :param shifts:
    :type shifts: dict
    :param sales:
    :type sales: dict
    :return: A dictionary with time as key (string) with format %H:%M and
    percentage of sales per labour cost as value (float),
    If the sales are null, then return -cost instead of percentage
    For example, it should be something like :
    {
        "17:00": 20,
        "22:00": -40,
    }
    :rtype: dict
    """
    # Initialise result dictionary.
    result = {}
    for x in shifts:
        result[x] = 0

    # Filling result with data.
    for y in result:
        # Try to obtain costs.
        try:
            costs = shifts[y]
        except:
            costs = 0

        # Try to obtain sale value.
        try:
            sale = sales[y]
        except:
            sale = 0
        if costs > sale:
            # Reverting to negative value.
            result[y] = float("-" + str(costs))
        if costs < sale:
            # Calculate percentage. Two steps for clarity.
            anInt = (costs * 100)
            anInt = anInt / sale
            # Cost of labour compared to sales. Rounded to two decimal points.
            result[y] = round(anInt, 2)
    return result


def best_and_worst_hour(percentages):
    """

    Args:
    percentages: output of compute_percentage
    Return: list of strings, the first element should be the best hour,
    the second (and last) element should be the worst hour. Hour are
    represented by string with format %H:%M
    e.g. ["18:00", "20:00"]

    """
    # Initial setup of variable, so they should be easily swapped.
    bestHour = 100  # <-- init to 100% of labour
    bestHourKey = ""
    worstHour = -1  # <-- init to min lose
    worstHourKey = ""

    for x in percentages:
        value = percentages[x]
        if value > 0:
            if value < bestHour:
                bestHour = value
                bestHourKey = x
        if value < 0:
            if value < worstHour:
                worstHour = value
                worstHourKey = x

    # Creation of list for result variable.
    result = []
    result.append(bestHourKey)
    result.append(worstHourKey)

    return result


def main(path_to_shifts, path_to_sales):
    """
    Do not touch this function, but you can look at it, to have an idea of
    how your data should interact with each other
    """

    shifts_processed = process_shifts(path_to_shifts)
    sales_processed = process_sales(path_to_sales)
    percentages = compute_percentage(shifts_processed, sales_processed)
    best_hour, worst_hour = best_and_worst_hour(percentages)
    return best_hour, worst_hour


if __name__ == '__main__':
    # You can change this to test your code, it will not be used
    path_to_sales = os.path.abspath('transactions.csv')
    path_to_shifts = os.path.abspath('work_shifts.csv')
    # best_hour, worst_hour = main(path_to_shifts, path_to_sales)
    process_shifts(path_to_shifts)
    # added for tests
    process_sales(path_to_sales)
    best_and_worst_hour(compute_percentage(process_shifts(path_to_shifts), process_sales(path_to_sales)))

# Please write you name here: KRZYSZTOF SZUMKO
