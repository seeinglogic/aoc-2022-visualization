async function drawGraph() {

  // Pick which JSON to use
  //const data_file = "./day12-wrong.json"
  const data_file = "./day12-right.json"
  
  const dataset = await d3.json(data_file)


  // dimensions, bounds, svg
  const width = 1200
  let dimensions = {
    width: width,
    height: width * 0.6,
    margin: {
      top: 10,
      right: 10,
      bottom: 10,
      left: 10,
    },
  }
  dimensions.boundedWidth = dimensions.width - dimensions.margin.left - dimensions.margin.right
  dimensions.boundedHeight = dimensions.height - dimensions.margin.top - dimensions.margin.bottom

  const wrapper = d3.select("#wrapper")
    .append("svg")
      .attr("width", dimensions.width)
      .attr("height", dimensions.height)

  const bounds = wrapper.append("g")
      .style("transform", `translate(${dimensions.margin.left}px, ${dimensions.margin.top}px)`)

  
  // accessors and scales
  const xAccessor = d => +d.x
  const yAccessor = d => +d.y
  const heightAccessor = d => d.height
  const coveredAccessor = d => d.covered

  const xScale = d3.scaleLinear()
    .domain(d3.extent(dataset, xAccessor))
    .range([0, dimensions.boundedWidth])
    .nice()

  const yScale = d3.scaleLinear()
    .domain(d3.extent(dataset, yAccessor))
    .range([dimensions.boundedHeight, 0])
    .nice()
  
  function getOrdinal(c) {
      return c.charCodeAt(0) - 97  // 97 is 0x61 or 'a'
  }
  const blueScale = d3.scaleLinear()
    .domain([getOrdinal('a'), getOrdinal('z')])
    .range([d3.interpolateBlues(0.1), d3.interpolateBlues(1)])


  function colorMap(height) {
    if (height == 'S') {
      return '#00ff00'
    }
    if (height == 'E') {
      return '#ff0000'
    }
    else {
      return blueScale(getOrdinal(height))
    }
  }

  function coveredMap(covered) {
    if (covered) {
      return 'purple'
    } 
    return ''
  }


  // Draw data
  const squarePadding = 2
  const numSquaresWide = d3.max(dataset, xAccessor)
  const numSquaresTall = d3.max(dataset, yAccessor)
  const rectWidth = dimensions.boundedWidth / numSquaresWide - squarePadding
  const rectHeight = dimensions.boundedHeight / numSquaresTall - squarePadding

  const nodeGroups = bounds.selectAll("rect")
      .data(dataset)
    .enter()
      .append("g")
        .attr("class", "node")

  const squareGroups = bounds.selectAll(".node")
      .append("rect")
        .attr("class", "square")
        .attr("x", d => xScale(xAccessor(d)) + squarePadding / 2)
        .attr("y", d => yScale(yAccessor(d)) + squarePadding / 2 - (rectHeight/2))
        .attr("width", rectWidth )
        .attr("height", rectHeight )
        .attr("fill", d => colorMap(heightAccessor(d)))
        .attr("stroke", d => coveredMap(coveredAccessor(d)))

  const textGroups = bounds.selectAll(".node")
      .append("text")
        .attr("x", d => xScale(xAccessor(d)) + rectWidth / 2 + squarePadding / 2)
        .attr("y", d => yScale(yAccessor(d)) + rectHeight / 3)
        .attr("fill", "#202020")
        .style("font-size", "0.6em")
        .style("font-weight", "700")
        .style("text-anchor", "middle")
        .html(d => heightAccessor(d))
}

drawGraph()
