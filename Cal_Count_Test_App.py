from kivy.app import App
from kivy.event import EventDispatcher
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from Cal_Dict_Test import Calorie_Dict
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.popup import Popup
import random
import re

class search_button(Button):
    search_button_id = NumericProperty(1)

class SearchGrid(GridLayout, EventDispatcher):
    search_id = NumericProperty(1)
    search_name = StringProperty()
    search_value = NumericProperty(1)
    search_values = StringProperty()


class IdGrid(GridLayout, EventDispatcher):
    grid_id = NumericProperty(1)


class ContentTab(TabbedPanel):
    pass


class CalTotalScreen(GridLayout):
    global CalTotalList
    global cal_final_count
    cal_final_count = []
    CalTotalList = [("McBiscuit", 330), ("McBiscuit", 330), ("McBiscuit", 330), ("McBiscuit", 330), ("McNuggets", 430), ("McNuggets", 430), ("McNuggets", 430), ("McGriddle", 560), ("McGriddle", 560), ("McGriddle", 560)]

    def calculate_total_calories(self, inputnumber):
        if inputnumber == 0:
            calorie_total = 0
            for number in cal_final_count:
                calorie_total += number
            return calorie_total
        if inputnumber == 1:
            while cal_final_count:
                cal_final_count.pop(0)

    def remove_rows(self):
        self.ids.cal_home_item_grid.clear_widgets([row for row in self.ids.cal_home_item_grid.children])
        self.calculate_total_calories(1)
        self.ids.final_calorie_label.text = "0"
        self.iterate_row_id(0)
        while CalTotalList:
            CalTotalList.pop(0)

    def clear_rows_cal_screen(self):
        self.ids.cal_home_item_grid.clear_widgets([row for row in self.ids.cal_home_item_grid.children])
        self.calculate_total_calories(1)
        self.iterate_row_id(0)

    def remove_bottom_row(self): # take row num and remove from interface/cal_final_count/caltotallist
        current_last_row = int(self.iterate_row_id(2)) - 1
        if current_last_row > 0:
            current_last_row_cal_count = current_last_row - 1
            current_last_row_total_list = current_last_row - 1
            cal_final_count.pop(current_last_row_cal_count)
            CalTotalList.pop(current_last_row_total_list)
            for child in self.ids.cal_home_item_grid.children:
                if child.grid_id == current_last_row:
                    self.ids.cal_home_item_grid.remove_widget(child)
            self.iterate_row_id(3)
            self.ids.final_calorie_label.text = str(self.calculate_total_calories(0))
        elif current_last_row==1:
            self.ids.cal_home_item_grid.remove_widget(1)
            cal_final_count.remove(0)
            CalTotalList.remove(0)
            self.iterate_row_id(3)
            self.ids.final_calorie_label.text = str(self.calculate_total_calories(0))
        else:
            pass

    def iterate_row_id(self, inputnumber=2):
        global current_row_id
        if inputnumber == 0:
            current_row_id = 1  # reset value
            print("reset value: " + str(current_row_id))
        if inputnumber == 1:
            current_row_id += 1  # iterate by 1
            print("Iterate by 1: " + str(current_row_id))
        if inputnumber == 2:
            print("current row: " + str(current_row_id))
            return current_row_id  # return last row/current row
        if inputnumber == 3:
            current_row_id = current_row_id - 1  # remove bottom row
            print("remove bottom row: " + str(current_row_id))

    def refresh_cal_list(self):
        self.clear_rows_cal_screen()
        for itemname, itemvalue in CalTotalList:
            cal_home_label_text = str(itemvalue) + " Cal"
            row_id = IdGrid(cols=3, rows=1, size_hint=(1, None), height="50dp", grid_id=self.iterate_row_id(2))
            row_id.add_widget(Label(text=itemname))
            row_id.add_widget(Label(text=cal_home_label_text))
            row_id.add_widget(Button(text="remove", background_color=(1, 1, .5, 1)))
            cal_final_count.append(itemvalue)
            self.iterate_row_id(1)
            self.ids.cal_home_item_grid.add_widget(row_id)
        self.ids.final_calorie_label.text = str(self.calculate_total_calories(0)) + " Cal"



class SearchForItemScreen(GridLayout):

    def iterate_search_row_id(self, inputnumber):
        global current_search_row_id
        if inputnumber == 0:
            current_search_row_id = 0  # reset search row value
            print("reset search value: " + str(current_search_row_id))
        if inputnumber == 1:
            current_search_row_id += 1  # iterate search row by 1
            print("Iterate search value by 1: " + str(current_search_row_id))
        if inputnumber == 2:
            print("current search row value: " + str(current_search_row_id))
            return current_search_row_id  # return last row/current search row

    def clear_search_results(self): # rework to delete based on removing lowest ID?
        self.ids.search_results_grid.clear_widgets([row for row in self.ids.search_results_grid.children])
        self.iterate_search_row_id(0)

    def clear_search_list(self):
        search_result_load_list.clear()

    def load_search_results(self):
        for match in search_result_load_list:
            found_name = match
            found_value = Calorie_Dict[match]
            calorie_search_label = str(found_value) + " Cal"
            search_row = SearchGrid(cols=3, rows=1, size_hint=(1, None), height="50dp", search_name=found_name,
                                    search_value=found_value, search_id=self.iterate_search_row_id(2))
            search_row.add_widget(Label(text=found_name, size_hint_x=.5))
            search_row.add_widget(Label(text=calorie_search_label, size_hint_x=.25))
            new_button = search_button(text="Add to List", size_hint_x=.25, search_button_id=self.iterate_search_row_id(2))
            new_button.bind(on_press=self.add_row_value_to_cal_list)
            search_row.add_widget(new_button)
            self.ids.search_results_grid.add_widget(search_row)
            self.iterate_search_row_id(1)

    def get_text_from_search_bar(self):
        global search_result_load_list
        self.clear_search_results()
        search_result_load_list = []
        self.clear_search_list()
        current_text = self.ids.search_text_input.text
        print(current_text)
        search_pattern = re.compile(current_text, re.IGNORECASE)
        for key in Calorie_Dict.keys():
            s_match = search_pattern.match(key)
            if s_match:
                print('Match found: ', s_match.group())
                search_result_load_list.append(key)
        print(search_result_load_list)
        self.load_search_results()

    def add_search_result_to_cal_list(self, widget): # function currently phased out right now/unused
        search_num_to_add = widget.search_button_id
        for child in self.ids.search_results_grid.children:
            if child.search_id == search_num_to_add:
                packed_result = (child.search_name, child.search_value)
                CalTotalList.append(packed_result)
                cal_final_count.append(child.search_value)

    def add_row_value_to_cal_list(self, instance): # function runs without any arguments/need to grab row_id
        new_search_num = 2
        for child in self.ids.search_results_grid.children:
            if child.search_id == new_search_num:
                packed_result = (child.search_name, child.search_value)
                CalTotalList.append(packed_result)
                cal_final_count.append(child.search_value)
                print("Added: " + str(child.search_name) + " to the global list")



class CalApp(App):
    caltotal = CalTotalScreen()
    caltotal.iterate_row_id(0)
    searchscreen = SearchForItemScreen()
    searchscreen.iterate_search_row_id(0)
    pass


if __name__ == "__main__":
    CalApp().run()
