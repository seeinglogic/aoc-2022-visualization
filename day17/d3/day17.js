
async function drawChart(dataset, color, i) {

  const yAccessor = d => +d.y
  const xAccessor = d => +d.x
  const blockNumAccessor = d => +d.i
  const heightAccessor = d => +d.height
  const blockTypeAccessor = d => d.block_type


  // dimensions and framing
  let dimensions = {
    width: 200,
    height: window.innerHeight * 0.75,
    margin: {
      top: 15,
      right: 25,
      bottom: 60,
      left: 40,
    },
  }
  dimensions.boundedWidth = dimensions.width
    - dimensions.margin.left
    - dimensions.margin.right
  dimensions.boundedHeight = dimensions.height
    - dimensions.margin.top
    - dimensions.margin.bottom


  // create the svg and wrapper group
  const wrapper = d3.select("#wrapper")
    .append("svg")
      .attr("width", dimensions.width)
      .attr("height", dimensions.height)

  const bounds = wrapper.append("g")
      .style("transform", `translate(${
        dimensions.margin.left
      }px, ${
        dimensions.margin.top
      }px)`)


  // make scales
  const xScale = d3.scaleLinear()
    .domain([-0.5, 6.5])
    .range([0, dimensions.boundedWidth])

  const yScale = d3.scaleLinear()
    .domain(d3.extent(dataset, yAccessor))
    .range([dimensions.boundedHeight, 0])
    .nice()


  // draw squares
  const squareSize = 4;
  let getSquareX = d => xScale(xAccessor(d)) - squareSize/2 + 0.5;
  let getSquareY = d => yScale(yAccessor(d)) - squareSize

  bounds.selectAll("rect")
      .data(dataset)
    .join("rect")
      .attr("x", d => getSquareX(d))
      .attr("y", d => getSquareY(d))
      .attr("height", squareSize)
      .attr("width", squareSize)
      .attr("fill", color)


  // draw axes
  const yAxisGenerator = d3.axisLeft()
    .scale(yScale)
  const yAxis = bounds.append("g")
    .call(yAxisGenerator)

  const xAxisGenerator = d3.axisBottom()
    .tickValues([0, 1, 2, 3, 4, 5, 6])
    .tickFormat(d => d.toString())
    .scale(xScale)
  const xAxis = bounds.append("g")
    .call(xAxisGenerator)
      .style("transform", `translateY(${
        dimensions.boundedHeight
      }px)`)
  
  const shapeName = blockTypeAccessor(dataset[0])
  const xAxisLabel = xAxis.append("text")
      .attr("x", dimensions.boundedWidth / 2)
      .attr("y", dimensions.margin.bottom - 20)
      .attr("fill", "black")
      .style("font-size", "1.5em")
      .text(`Shape: ${shapeName}`)
      .style("text-transform", "capitalize")


  // make hitboxes for tooltip summoning
  const delaunay = d3.Delaunay.from(
    dataset,
    d => xScale(xAccessor(d)),
    d => yScale(yAccessor(d)),
  )
  const voronoi = delaunay.voronoi()
  voronoi.xmax = dimensions.boundedWidth
  voronoi.ymax = dimensions.boundedHeight

  bounds.selectAll(".voronoi")
    .data(dataset)
    .enter().append("path")
      .attr("class", "voronoi")
      .attr("d", (d,i) => voronoi.renderCell(i))
      //.attr("stroke", "salmon")
      .on("mouseenter", onMouseEnter)
      .on("mouseleave", onMouseLeave)


  // event handling for tooltip summoning
  const tooltip = d3.select("#tooltip")
  function onMouseEnter(datum) {
    const highlightSquare = bounds.append("rect")
        .attr("class", "tooltipSquare")
        .attr("x", d => getSquareX(datum))
        .attr("y", d => getSquareY(datum))
        .attr("height", squareSize)
        .attr("width", squareSize)
        .style("fill", "springgreen")
        .style("pointer-events", "none")

    tooltip.select("#x")
        .text(`${xAccessor(datum)}`)
    tooltip.select("#y")
        .text(`${yAccessor(datum)}`)

    tooltip.select("#blocknum")
        .text(blockNumAccessor(datum))
    tooltip.select("#height")
        .text(heightAccessor(datum))

    const x = i * dimensions.width
      + dimensions.margin.left
      + getSquareX(datum)
      + squareSize / 2

    const y = dimensions.margin.top 
      + getSquareY(datum)

    tooltip.style("transform", `translate(`
      + `calc( -50% + ${x}px),`
      + `calc(-100% + ${y + squareSize}px)`
      + `)`)

    tooltip.style("opacity", 1)
  }

  function onMouseLeave() {
    d3.selectAll(".tooltipSquare")
      .remove()

    tooltip.style("opacity", 0)
  }
}


async function drawCharts() {
  // Best graph here is a separate graph for each type

  let dataset = await d3.json("./day17.json")
  //dataset = dataset.slice(0,5000)

  let shapes = {
    '-': 'cornflowerblue',
    '+': 'red',
    'L': 'green',
    'I': 'blue',
    'x': 'purple',
  }

  let i = 0;
  for (let [shape, color] of Object.entries(shapes)) {
    const shapeData = dataset.filter((d) => d.block_type == shape);
    drawChart(shapeData, color, i)    
    i += 1;
  }
}

drawCharts()
