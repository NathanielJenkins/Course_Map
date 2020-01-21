// trigger the submit button on load for CSC 361 as default

$( document ).ready(function() {
  $.get( "/get_prereq/", "cid=CSC%20361",  data => loadGraph(data))
});

$( "#course_form" ).submit(function( event ){
  event.preventDefault()
  $.get( "/get_prereq/", $(this).serialize(),  data => loadGraph(data));
});

function loadGraph( data ){
  // set the top text
  if (!data.nodes) {
    $('#cid-title').text('NOT FOUND')
    $('#cid-title').css("color", "salmon")
    $('#cid-title').effect("shake")
    return
  }
  $('#cid-title').css("color", "white")
  $('#cid-title').text(data.nodes[0].data.name)
  
  var cy = window.cy = cytoscape({
    container: document.getElementById('cy'),
      
    style: [
      {
        selector: 'node',
        css: {
          'content': 'data(name)',
          'text-valign': 'center',
          'text-halign': 'center',
          'shape' : 'rectangle',
          'background-color' : "LightSalmon",
          'color' : "DarkSlateGray"
        }
      },
      {
        selector: ':parent',
        css: {
          'text-valign': 'top',
          'text-halign': 'center',
          'background-color' : "LightSteelBlue",
          'border-color' : "DarkSlateGray"
          
        }
      },
      {
        selector: ':child',
        css: {
          'background-color' : "SteelBlue",
          'color' : 'white'

        }
      },
      {
        selector: 'edge',
        css: {
          'line-color' : "grey",
          'target-arrow-color': 'grey',
          "width": 2,
          'curve-style': 'bezier',
          'target-arrow-shape': 'vee',
          'line-style' : 'dashed'

        }
      },
      {
        selector: '.hidden',
        css: {
          'opacity': 0,
        }
      },
    ],
  
    elements: {
      nodes: data.nodes,
      edges: data.edges
    },
  
    layout: {
      name: 'dagre',
      padding: 100,
    }
  });
}