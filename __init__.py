import octoprint.plugin
import requests
import json
import time

class HandCodePlugin(octoprint.plugin.SettingsPlugin,
                     octoprint.plugin.AssetPlugin,
                     octoprint.plugin.TemplatePlugin,
                     octoprint.plugin.SimpleApiPlugin):

    def get_settings_defaults(self):
        return {
            "handcode_url": "http://localhost:8000",
            "z_up": 5,
            "z_down": -1.5,
            "font_size": 25,
            "style": 0,
            "legibility": 0.8,
            "rotation": 0,
            "bed_width": 200,
            "bed_depth": 200
        }

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=True),
            dict(type="tab", custom_bindings=True)
        ]

    def get_assets(self):
        return {
            "js": ["js/handcode.js"],
            "css": ["css/handcode.css"]
        }

    def get_api_commands(self):
        return {
            "generate_gcode": [],
            "batch_generate": []
        }

    def on_api_command(self, command, data):
        if command == "generate_gcode":
            return self._generate_gcode(data)
        elif command == "batch_generate":
            return self._batch_generate(data)

    def _generate_gcode(self, data):
        url = self._settings.get(["handcode_url"])
        payload = {
            "text": data.get("text"),
            "font_size": data.get("font_size"),
            "style": data.get("style"),
            "legibility": data.get("legibility"),
            "pen": {
                "z_up": data.get("z_up"),
                "z_down": data.get("z_down")
            },
            "rotation": data.get("rotation"),
            "offset": {
                "x": data.get("offset_x"),
                "y": data.get("offset_y")
            }
        }

        try:
            response = requests.post(f"{url}/task", json=payload)
            response.raise_for_status()
            task_id = response.json()["taskid"]
            
            gcode = self._poll_for_gcode(url, task_id)
            if gcode:
                filename = f"handcode_{int(time.time())}.gcode"
                self._printer.inject_gcode(gcode, filename=filename)
                return {"success": True, "filename": filename}
            else:
                return {"success": False, "error": "Failed to retrieve GCode."}

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def _batch_generate(self, data):
        lines = data.get("csv_data").splitlines()
        for line in lines:
            parts = line.split(',')
            if len(parts) >= 2:
                text = parts[0]
                style = int(parts[1]) if len(parts) > 1 else self._settings.get(["style"])
                font_size = int(parts[2]) if len(parts) > 2 else self._settings.get(["font_size"])
                
                job_data = {
                    "text": text,
                    "style": style,
                    "font_size": font_size,
                    "z_up": self._settings.get(["z_up"]),
                    "z_down": self._settings.get(["z_down"]),
                    "legibility": self._settings.get(["legibility"]),
                    "rotation": self._settings.get(["rotation"]),
                    "offset_x": 0,
                    "offset_y": 0,
                }
                self._generate_gcode(job_data)
        return {"success": True}

    def _poll_for_gcode(self, url, task_id):
        for _ in range(30):  # Poll for 30 seconds
            try:
                response = requests.get(f"{url}/task/{task_id}")
                response.raise_for_status()
                data = response.json()
                if data["status"] == "done":
                    return data["gcode"]
                elif data["status"] == "error":
                    return None
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        return None

__plugin_name__ = "HandCode"
__plugin_version__ = "1.0.0"
__plugin_description__ = "Generate handwriting GCode with HandCode"
__plugin_implementation__ = HandCodePlugin()
