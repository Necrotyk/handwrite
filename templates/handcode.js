$(function() {
    function HandCodeViewModel(parameters) {
        var self = this;

        self.settings = parameters[0];
        
        self.text_input = ko.observable("Hello from OctoPrint!");
        self.font_size = ko.observable(25);
        self.style = ko.observable(0);
        self.rotation = ko.observable(0);

        self.paper_width = ko.observable(150);
        self.paper_height = ko.observable(100);

        self.bed_width = ko.pureComputed(function() {
            return self.settings.settings.plugins.handcode.bed_width();
        });
        self.bed_depth = ko.pureComputed(function() {
            return self.settings.settings.plugins.handcode.bed_depth();
        });

        self.batch_input = ko.observable("");

        self.generateGCode = function() {
            var paper = $("#paper");
            var position = paper.position();
            
            OctoPrint.simpleApiCommand("handcode", "generate_gcode", {
                text: self.text_input(),
                font_size: self.font_size(),
                style: self.style(),
                legibility: self.settings.settings.plugins.handcode.legibility(),
                z_up: self.settings.settings.plugins.handcode.z_up(),
                z_down: self.settings.settings.plugins.handcode.z_down(),
                rotation: self.rotation(),
                offset_x: position.left,
                offset_y: position.top
            })
            .done(function(response) {
                if(response.success) {
                    new PNotify({
                        title: 'GCode Generated',
                        text: 'Successfully generated ' + response.filename,
                        type: 'success'
                    });
                }
            });
        };
        
        self.runBatch = function() {
             OctoPrint.simpleApiCommand("handcode", "batch_generate", {
                csv_data: self.batch_input()
             });
        };

        // Make the paper draggable
        $("#paper").draggable({
            containment: "#bed_visualizer"
        });
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: HandCodeViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#tab_handcode", "#settings_handcode"]
    });
});
