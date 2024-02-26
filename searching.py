import pandas as pd
import random

class Searching:
    def __init__(self):
        self.locations = [(floor, apartment) for floor in range(1, 9) for apartment in range(1, 6)]
        self.apartments = pd.DataFrame(self.locations, columns=['Floor', 'Apartment'])
        self.apartments['Broken Window'] = False
        self.apartments['Broken Lock'] = False
        self.apartments['Both Broken'] = False
        self.intrusion_records = []

    def heuristic(self, start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    def get_neighbors(self, current):
        neighbors = []
        for floor, apartment in self.locations:
            if (floor == current[0] and abs(apartment - current[1]) == 1) or (
                    apartment == current[1] and abs(floor - current[0]) == 1):
                neighbors.append((floor, apartment))
        return neighbors

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def get_output(self):
        output = ""

        intrusion_index = random.randint(0, len(self.locations) - 1)

        self.apartments.loc[intrusion_index, 'Broken Window'] = random.choice([True, False])
        self.apartments.loc[intrusion_index, 'Broken Lock'] = random.choice([True, False])

        if (self.apartments.loc[intrusion_index, 'Broken Window'] == False) & (
                self.apartments.loc[intrusion_index, 'Broken Lock'] == False):
            output += "\nThere was no Break-In found!!\nYour Apartment Building is Safe :))\n"
        else:
            self.apartments.loc[
                (self.apartments['Broken Window'] == True) & (self.apartments['Broken Lock'] == True),
                'Both Broken'] = True

            filtered_apartments = self.apartments.loc[
                (self.apartments['Broken Window'] == True) | (self.apartments['Broken Lock'] == True)]

            output += "Found the Intrusion at:\n"
            for _, apartment in filtered_apartments.iterrows():
                output += f"Floor: {apartment['Floor']}, Apartment: {apartment['Apartment']}\n"

            floor_to_evacuate = self.apartments.loc[intrusion_index, 'Floor']
            output += "\nPLEASE EVACUATE THE " + str(floor_to_evacuate) + "th FLOOR\n"

            output += "\nShortest Path to the Apartment Intrusion is found at:\n"
            for _, apartment in filtered_apartments.iterrows():
                start_apartment = (1, 1)
                end_apartment = (apartment['Floor'], apartment['Apartment'])

                open_set = [start_apartment]
                came_from = {}
                g_score = {start_apartment: 0}
                f_score = {start_apartment: self.heuristic(start_apartment, end_apartment)}

                while open_set:
                    current = min(open_set, key=lambda x: f_score[x])

                    if current == end_apartment:
                        path = self.reconstruct_path(came_from, current)
                        output += f"Path to Floor: {end_apartment[0]}, Apartment: {end_apartment[1]}: {path}\n"
                        break

                    open_set.remove(current)
                    for neighbor in self.get_neighbors(current):
                        tentative_g_score = g_score[current] + 1
                        if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                            came_from[neighbor] = current
                            g_score[neighbor] = tentative_g_score
                            f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end_apartment)
                            if neighbor not in open_set:
                                open_set.append(neighbor)

        return output

