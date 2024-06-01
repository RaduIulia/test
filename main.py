from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from plyer import accelerometer, compass
import csv

class SensorDisplay(BoxLayout):
    def __init__(self, **kwargs):
        super(SensorDisplay, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.accel_label = Label(text='Accelerometer Data:\nX: 0\nY: 0\nZ: 0')
        self.compass_label = Label(text='Compass Data:\nX: 0\nY: 0\nZ: 0')

        self.add_widget(self.accel_label)
        self.add_widget(self.compass_label)

        self.start_button = Button(text='Start')
        self.start_button.bind(on_press=self.start_recording)
        self.add_widget(self.start_button)

        self.stop_button = Button(text='Stop')
        self.stop_button.bind(on_press=self.stop_recording)
        self.add_widget(self.stop_button)

        self.recording = False
        self.sensor_data = []

        # Schedule the sensor updates
        Clock.schedule_interval(self.update_sensors, 1.0 / 20.0)  # Update at 20 Hz

    def start_recording(self, instance):
        self.recording = True

    def stop_recording(self, instance):
        self.recording = False
        self.save_data()

    def update_sensors(self, dt):
        try:
            accel_data = accelerometer.acceleration
            if accel_data:
                self.accel_label.text = f'Accelerometer Data:\nX: {accel_data[0]:.2f}\nY: {accel_data[1]:.2f}\nZ: {accel_data[2]:.2f}'
        except NotImplementedError:
            self.accel_label.text = 'Accelerometer not implemented on this platform'

        try:
            compass_data = compass.orientation
            if compass_data:
                self.compass_label.text = f'Compass Data:\nX: {compass_data[0]:.2f}\nY: {compass_data[1]:.2f}\nZ: {compass_data[2]:.2f}'
        except NotImplementedError:
            self.compass_label.text = 'Compass not implemented on this platform'

        if self.recording:
            self.sensor_data.append({
                'accel_x': accel_data[0] if accel_data else None,
                'accel_y': accel_data[1] if accel_data else None,
                'accel_z': accel_data[2] if accel_data else None,
                'compass_x': compass_data[0] if compass_data else None,
                'compass_y': compass_data[1] if compass_data else None,
                'compass_z': compass_data[2] if compass_data else None,
            })

    def save_data(self):
        with open('accelerometer_data.csv', 'w', newline='') as csvfile:
            fieldnames = ['accel_x', 'accel_y', 'accel_z']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for data in self.sensor_data:
                writer.writerow({
                    'accel_x': data['accel_x'],
                    'accel_y': data['accel_y'],
                    'accel_z': data['accel_z']
                })

        with open('compass_data.csv', 'w', newline='') as csvfile:
            fieldnames = ['compass_x', 'compass_y', 'compass_z']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for data in self.sensor_data:
                writer.writerow({
                    'compass_x': data['compass_x'],
                    'compass_y': data['compass_y'],
                    'compass_z': data['compass_z']
                })

        # Clear the data after saving
        self.sensor_data = []

class SensorApp(App):
    def build(self):
        return SensorDisplay()

if __name__ == '__main__':
    SensorApp().run()
