function draw_path(roteiro) {
    var svg = d3.select('svg');
    var circles = [];
    var lineData = [];

    for (var i in roteiro['sequence']) {
        var part = roteiro['sequence'][i];
        var vid = String(part['vid']);
        var path = d3.select(`[data-vid='${vid}']`);
        if (path.node()) {
            var bbox = path.node().getBBox();
            var new_circle = {'cx': bbox['x'] + bbox['width']/2.0,
                              'cy': bbox['y'] + bbox['height']/2.0,
                              'r': bbox['width']/2.0 + 3
                             };
            circles.push(new_circle);
            svg.insert("circle", ":first-child").attr("cx", new_circle["cx"]).attr("cy", new_circle["cy"]).attr("r", new_circle['r']).attr("fill-opacity", "0").attr("transform", "translate(-43.97 -36.95)");
        }

        lineData.push({'x': new_circle['cx'], 'y': new_circle['cy']});
    }

    var lineFunction = d3.svg.line().x(function(d) { return d.x;  }).y(function(d) { return d.y;  }).interpolate("linear");
    svg.insert("path").attr("d", lineFunction(lineData)).attr("stroke", "black").attr("transform", "translate(-43.97 -36.95)").attr("stroke-width", 4).attr("fill", "none");

}
