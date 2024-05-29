import tkinter as tk
import paho.mqtt.client as mqtt
import json
import math

broker_address = "mqtt.ics.ele.tue.nl"
topic_subscribe = "/pynqbridge/23/send"
username = "Student45"  # Replace with your MQTT username
password = "di1BuX2i"  # Replace with your MQTT password

class CoordinateSystem(tk.Canvas):
    def __init__(self, master=None, width=600, height=600, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.create_line(0, height / 2, width, height / 2, fill="black")  # X-axis
        self.create_line(width / 2, 0, width / 2, height, fill="black")  # Y-axis
        self.origin = (width / 2, height / 2)  # Coordinate system origin
        self.x_scale = 4
        self.y_scale = 4
        self.legend_items = [
            ("Cliff", "black", "circle"),
            ("Hill", "blue", "hexagon"),
            ("Small Rock", "red", "square", 10),
            ("Big Rock", "green", "square", 30)
        ]

    def plot_point(self, x, y, color="red", shape="oval", size=2, tag=None):
        scaled_x = self.origin[0] + x * self.x_scale
        scaled_y = self.origin[1] - y * self.y_scale
        
        if shape == "oval":
            item = self.create_oval(scaled_x - size, scaled_y - size, scaled_x + size, scaled_y + size, fill=color, tags=tag)
        elif shape == "rectangle":
            item = self.create_rectangle(scaled_x - size, scaled_y - size, scaled_x + size, scaled_y + size, fill=color, tags=tag)
        elif shape == "hexagon":
            item = self.draw_hexagon(scaled_x, scaled_y, size, color, tag)
        elif shape == "long_rectangle":
            item = self.create_rectangle(scaled_x - size, scaled_y - size/2, scaled_x + size, scaled_y + size/2, fill=color, tags=tag)
        
        if tag == 'robot':
            self.after(5000, lambda: self.delete(item))

    def draw_hexagon(self, x, y, size, color, tag):
        angle = 60
        points = []
        for i in range(6):
            angle_rad = math.radians(angle * i)
            point_x = x + size * math.cos(angle_rad)
            point_y = y + size * math.sin(angle_rad)
            points.append(point_x)
            points.append(point_y)
        return self.create_polygon(points, outline=color, fill=color, tags=tag)

    def draw_axis_labels(self):
        for i in range(-self.width // (2 * self.x_scale), self.width // (2 * self.x_scale) + 1, 5):
            if i % 15 == 0:  # Only draw labels when the number is a multiple of 5
                x = self.origin[0] + i * self.x_scale
                self.create_text(x, self.origin[1] + 10, text=str(i), anchor=tk.N)
        for i in range(-self.height // (2 * self.y_scale), self.height // (2 * self.y_scale) + 1, 5):
            if i % 15 == 0:  # Only draw labels when the number is a multiple of 5
                y = self.origin[1] - i * self.y_scale
                self.create_text(self.origin[0] - 10, y, text=str(i), anchor=tk.E)

    def draw_legend(self):
        self.create_text(self.width - 50, 50, text="Legend:", anchor=tk.N)
        y_offset = 70
        for item in self.legend_items:
            label, color, shape, size = item[:4] if len(item) > 3 else (item[0], item[1], item[2], 5)
            legend_text = f"{label}: {shape.capitalize()}"
            self.create_text(self.width - 50, y_offset, text=legend_text, fill=color, anchor=tk.N)
            y_offset += 20

class CoordinateSystemApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Coordinate System")

        self.coordinate_system = CoordinateSystem(master, width=600, height=600)
        self.coordinate_system.pack()

        # Draw axis labels
        self.coordinate_system.draw_axis_labels()

        # Draw legend
        self.coordinate_system.draw_legend()

        # Create an MQTT client instance
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect to the MQTT broker
        self.client.connect(broker_address)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            # Subscribe to the specified topic
            client.subscribe(topic_subscribe)
        else:
            print(f"Failed to connect, return code {rc}\n")

    def on_message(self, client, userdata, message):
        json_data = json.loads(message.payload.decode('utf-8'))
        typeObject = json_data.get('type')
        x = json_data.get('x', 0)  # Default to 0 if 'x' key is not found
        y = json_data.get('y', 0)  # Default to 0 if 'y' key is not found

        match typeObject:
            case 'cliff':
                color = 'white'
                shape = 'oval'
                size = json_data.get('size', 10)
                tag = ''
            case 'hill':
                color = 'black'
                shape = 'hexagon'
                size = json_data.get('size', 10)
                tag = ''
            case 'robot':
                color = 'gray'
                shape = 'long_rectangle'
                size = json_data.get('size', 20)
                tag = 'robot'
            case 'Lrblue':
                color = 'blue'
                shape = 'rectangle'
                size = json_data.get('size', 10)
                tag = ''
            case 'Lrgreen':
                color = 'green'
                shape = 'rectangle'
                size = json_data.get('size', 10)
                tag = ''
            case 'Lrblack':
                color = 'black'
                shape = 'rectangle'
                size = json_data.get('size', 10)
                tag = ''
            case 'Lrred':
                color = 'red'
                shape = 'rectangle'
                size = json_data.get('size', 10)
                tag = ''
            case 'Lrwhite':
                color = 'white'
                shape = 'rectangle'
                size = json_data.get('size', 10)
                tag = ''
            case 'Srblue':
                color = 'blue'
                shape = 'rectangle'
                size = json_data.get('size', 5)
                tag = ''
            case 'Srgreen':
                color = 'green'
                shape = 'rectangle'
                size = json_data.get('size', 5)
                tag = ''
            case 'Srblack':
                color = 'black'
                shape = 'rectangle'
                size = json_data.get('size', 5)
                tag = ''
            case 'Srred':
                color = 'red'
                shape = 'rectangle'
                size = json_data.get('size', 5)
                tag = ''
            case 'Srwhite':
                color = 'white'
                shape = 'rectangle'
                size = json_data.get('size', 5)
                tag = ''

        self.coordinate_system.plot_point(x, y, color=color, shape=shape, size=size, tag=tag)

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordinateSystemApp(root)
    root.mainloop()
