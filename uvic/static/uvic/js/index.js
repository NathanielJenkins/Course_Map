$( "#course_form" ).submit(function( event ){
  event.preventDefault()

  $.get( "/get_prereq/", $(this).serialize(),  function( data ) {
    console.log(data)

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
            'line-color' : "DarkSlateGray",
            'target-arrow-color': 'DarkSlateGray',
            "width": 1,
            'curve-style': 'bezier',
            'target-arrow-shape': 'vee'
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
        name: 'dagre'      
      }
    });
  });
});