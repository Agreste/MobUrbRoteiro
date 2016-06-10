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
                              'r': bbox['width']/2.0
                             };
            circles.push(new_circle);
            svg.insert("circle", ":first-child").attr("cx", new_circle["cx"]).attr("cy", new_circle["cy"]).attr("r", new_circle['r']).attr("fill-opacity", "0").attr("transform", "translate(-43.97 -36.95)");
        }

    }

    for (var i = 0; i < circles.length - 1; ++i) {
        var lx = circles[i + 1]['cx'] - circles[i]['cx'];
        var ly = circles[i + 1]['cy'] - circles[i]['cy'];
        var distance = Math.sqrt(Math.pow(lx,2) + Math.pow(ly, 2));
        var dx = circles[i]['r']*lx/distance;
        var dy = circles[i]['r']*ly/distance;
        lineData.push({'x': circles[i]['cx'] + dx, 'y': circles[i]['cy'] + dy});
        if (i == circles.length - 2) {
            var dx = circles[i + 1]['r']*lx/distance;
            var dy = circles[i + 1]['r']*ly/distance;
            lineData.push({'x': circles[i + 1]['cx'] - dx, 'y': circles[i + 1]['cy'] - dy});
        }
    }

    var lineFunction = d3.svg.line().x(function(d) { return d.x;  }).y(function(d) { return d.y;  }).interpolate("linear");
    svg.insert("path").attr("d", lineFunction(lineData)).attr("stroke", "black").attr("transform", "translate(-43.97 -36.95)").attr("stroke-width", 4).attr("fill", "none");

}
