from datetime import date

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from tasks import build


app = FastAPI()
app.mount("/download", StaticFiles(directory="download"), name="download")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        
        <head>
        <meta charset="utf-8">
        <script src="https://d3js.org/d3.v5.min.js"></script>
        <style>
        text{
            font-size: 16px;
            font-family: Open Sans, sans-serif;
        }
            text.title{
            font-size: 24px;
            font-weight: 500;
            }
            text.subTitle{
            font-weight: 500;
            fill: #777777;
            }
            text.caption{
            font-weight: 400;
            font-size: 14px;
            fill: #777777;
            }
            text.label{
            font-weight: 600;
            }

            text.valueLabel{
            font-weight: 300;
            }

            text.yearText{
            font-size: 64px;
            font-weight: 700;
            opacity: 0.25;
            }
            .tick text {
            fill: #777777;
            }
            .xAxis .tick:nth-child(2) text {
            text-anchor: start;
            }
            .tick line {
            shape-rendering: CrispEdges;
            stroke: #dddddd;
            }
            .tick line.origin{
            stroke: #aaaaaa;
            }
            path.domain{
            display: none;
            }
        </style>
        </head>

        <body>
        <script>
            // Feel free to change or delete any of the code you see in this editor!
            var svg = d3.select("body").append("svg")
        .attr("width", 960)
        .attr("height", 600);



        var tickDuration = 250;

        var top_n = 16;
        var height = 600;
        var width = 960;

        const margin = {
        top: 80,
        right: 0,
        bottom: 5,
        left: 0
        };

        let barPadding = (height-(margin.bottom+margin.top))/(top_n*5);

        let caption = svg.append('text')
        .attr('class', 'caption')
        .attr('x', width)
        .attr('y', height-5)
        .style('text-anchor', 'end')
        .html('Fecha');

        let year = 0.000;

        d3.csv('http://127.0.0.1:8000/download/province_confirmed_rank.csv').then(function(data) {
        //if (error) throw error;

        console.log(data);

        function getColor(value) {
            if (value == 'Pinar del Río')
                return "#00553d"
            else if (value == 'Artemisa')
                return "#fe0002"
            else if (value == 'La Habana')
                return "#020085"
            else if (value == 'Mayabeque')
                return "#940000"
            else if (value == 'Matanzas')
                return "#e36d70"
            else if (value == 'Cienfuegos')
                return "#00a261"
            else if (value == 'Villa Clara')
                return "#ff7a13"
            else if (value == 'Sancti Spíritus')
                return "#fe6515"
            else if (value == 'Ciego de Ávila')
                return "#008dd0"
            else if (value == 'Camagüey')
                return "#003060"
            else if (value == 'Las Tunas')
                return "#009c55"
            else if (value == 'Holguín')
                return "#007fc6"
            else if (value == 'Granma')
                return "#0b4ca0"
            else if (value == 'Santiago de Cuba')
                return "#ef242a"
            else if (value == 'Guantánamo')
                return "#515a57"
            else if (value == 'Isla de la Juventud')
                return "#38b396"
        }

        data.forEach(d => {
            d.value = +d.value,
            d.lastValue = +d.lastValue,
            d.value = isNaN(d.value) ? 0 : d.value,
            d.year = +d.year,
            d.colour = getColor(d.name)
        });

        console.log(data);

        let yearSlice = data.filter(d => d.year == year && !isNaN(d.value))
            .sort((a,b) => b.value - a.value)
            .slice(0, top_n);

        yearSlice.forEach((d,i) => d.rank = i);

        console.log('yearSlice: ', yearSlice)

        let x = d3.scaleLinear()
            .domain([0, d3.max(yearSlice, d => d.value)])
            .range([margin.left+150, width-margin.right-65]);

        let y = d3.scaleLinear()
            .domain([top_n, 0])
            .range([height-margin.bottom, margin.top]);

        let xAxis = d3.axisTop()
            .scale(x)
            .ticks(width > 500 ? 5:2)
            .tickSize(-(height-margin.top-margin.bottom))
            .tickFormat(d => d3.format(',')(d));

        svg.append('g')
            .attr('class', 'axis xAxis')
            .attr('transform', `translate(0, ${margin.top})`)
            .call(xAxis)
            .selectAll('.tick line')
            .classed('origin', d => d == 0);

        svg.selectAll('rect.bar')
            .data(yearSlice, d => d.name)
            .enter()
            .append('rect')
            .attr('class', 'bar')
            .attr('x', x(0)+1)
            .attr('width', d => x(d.value)-x(0)-1)
            .attr('y', d => y(d.rank)+5)
            .attr('height', y(1)-y(0)-barPadding)
            .style('fill', d => d.colour);

        svg.selectAll('text.label')
            .data(yearSlice, d => d.name)
            .enter()
            .append('text')
            .attr('class', 'label')
            .attr('x', d => x(d.value)-8)
            .attr('y', d => y(d.rank)+5+((y(1)-y(0))/2)+1)
            .style('text-anchor', 'end')
            .html(d => d.name);

        svg.selectAll('text.valueLabel')
            .data(yearSlice, d => d.name)
            .enter()
            .append('text')
            .attr('class', 'valueLabel')
            .attr('x', d => x(d.value)+5)
            .attr('y', d => y(d.rank)+5+((y(1)-y(0))/2)+1)
            .text(d => d3.format(',.0f')(d.lastValue));

        let yearText = svg.append('text')
            .attr('class', 'yearText')
            .attr('x', width-margin.right)
            .attr('y', height-25)
            .style('text-anchor', 'end')
            .html(~~year)
            .call(halo, 10);

        let ticker = d3.interval(e => {

            yearSlice = data.filter(d => d.year == year && !isNaN(d.value))
                .sort((a,b) => b.value - a.value)
                .slice(0,top_n);

            yearSlice.forEach((d,i) => d.rank = i);

            //console.log('IntervalYear: ', yearSlice);

            x.domain([0, d3.max(yearSlice, d => d.value)]); 

            svg.select('.xAxis')
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .call(xAxis);

            let bars = svg.selectAll('.bar').data(yearSlice, d => d.name);

            bars
                .enter()
                .append('rect')
                .attr('class', d => `bar ${d.name.replace(/\s/g,'_')}`)
                .attr('x', x(0)+1)
                .attr( 'width', d => x(d.value)-x(0)-1)
                .attr('y', d => y(top_n+1)+5)
                .attr('height', y(1)-y(0)-barPadding)
                .style('fill', d => d.colour)
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('y', d => y(d.rank)+5);

            bars
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('width', d => x(d.value)-x(0)-1)
                .attr('y', d => y(d.rank)+5);

            bars
                .exit()
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('width', d => x(d.value)-x(0)-1)
                .attr('y', d => y(top_n+1)+5)
                .remove();

            let labels = svg.selectAll('.label')
                .data(yearSlice, d => d.name);

            labels
                .enter()
                .append('text')
                .attr('class', 'label')
                .attr('x', d => x(d.value)-8)
                .attr('y', d => y(top_n+1)+5+((y(1)-y(0))/2))
                .style('text-anchor', 'end')
                .html(d => d.name)    
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('y', d => y(d.rank)+5+((y(1)-y(0))/2)+1);


            labels
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('x', d => 142)
                .attr('y', d => y(d.rank)+5+((y(1)-y(0))/2)+1);

            labels
                .exit()
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('x', d => x(d.value)-8)
                .attr('y', d => y(top_n+1)+5)
                .remove();


            let valueLabels = svg.selectAll('.valueLabel').data(yearSlice, d => d.name);

            valueLabels
                .enter()
                .append('text')
                .attr('class', 'valueLabel')
                .attr('x', d => x(d.value)+5)
                .attr('y', d => y(top_n+1)+5)
                .text(d => d3.format(',.0f')(d.lastValue))
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('y', d => y(d.rank)+5+((y(1)-y(0))/2)+1);

            valueLabels
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('x', d => x(d.value)+5)
                .attr('y', d => y(d.rank)+5+((y(1)-y(0))/2)+1)
                .tween("text", function(d) {
                    let i = d3.interpolateRound(d.lastValue, d.value);
                    return function(t) {
                    this.textContent = d3.format(',')(i(t));
                    };
                });


            valueLabels
                .exit()
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('x', d => x(d.value)+5)
                .attr('y', d => y(top_n+1)+5)
                .remove();

            function pretty_date(dias){
                var d = new Date(2020, 2, 11);
                d.setDate(d.getDate() + dias*1000);
                var day = d.getDate();
                var year = d.getFullYear();
                var month = d.getMonth();
                var options = {year: "numeric", month: "short", day: "numeric"};
                return (d.toLocaleDateString("es-ES", options));
            }

            yearText.html(pretty_date(year));

            if(year == 0.360) ticker.stop();
            year = d3.format('.3f')((+year) + 0.001);
        },tickDuration);

        });

        const halo = function(text, strokeWidth) {
        text.select(function() { return this.parentNode.insertBefore(this.cloneNode(true), this); })
            .style('fill', '#ffffff')
            .style('stroke','#ffffff')
            .style('stroke-width', strokeWidth)
            .style('stroke-linejoin', 'round')
            .style('opacity', 1);

        }   


        </script>
        </body>
    </html>
    """

@app.get("/build")
async def build_gifs():
    try:
        with open('download/update.txt') as f:
            update = date.fromisoformat(f.read())
            if date.today() > update:
                build.delay()
                return {"message": "Updating gifs"}
    except:
        build.delay()
        return {"message": "Updating gifs"}
    return {"message": "Updated gifs"}

@app.get('/download/<path:filename>')
async def download(filename):
    return StaticFiles('download/confirmed.gif')
