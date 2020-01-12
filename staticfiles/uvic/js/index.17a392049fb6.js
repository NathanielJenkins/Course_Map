$( "#course_form" ).submit(function( event ){
  event.preventDefault()

  $.get( "/get_prereq/", $(this).serialize(),  function( data ) {
    console.log(data)

    var cy = window.cy = cytoscape({
      container: document.getElementById('cy'),
    
      boxSelectionEnabled: false,
    
      style: [
        {
          selector: 'node',
          css: {
            'content': 'data(name)',
            'text-valign': 'center',
            'text-halign': 'center'
          }
        },
        {
          selector: ':parent',
          css: {
            'text-valign': 'top',
            'text-halign': 'center',
          }
        },
        {
          selector: 'edge',
          css: {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle'
          }
        }
      ],
    
      elements: {
        nodes: data.nodes,
        edges: data.edges
      },
    
      layout: {
        name: 'dagre',
      }
    });
  });
});