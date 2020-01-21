from .models import Course, Operation, PreCombinationCourse
import queue 

def find_req(cid): 
    courses = {
        "nodes" : [],
        "edges" : []
    }

    # breadth first search
    q = queue.Queue()

    # add start var
    level = 0;

    try:
        q.put (
            { 
                "course" : Course.objects.get(cid=cid),
                "operation" : Operation(operation="Single", id=None),
                "level" : level, 
                "parent" : None,
            }
        )
    except Course.DoesNotExist:
        return {}


    while q.qsize() != 0: 
        
        prereq_tuple = q.get()
        course = prereq_tuple['course']
        operation_1 = prereq_tuple['operation']

        # unique 
        courses['nodes'].append({
                "data" : {
                    "id" : course.cid + "-" + str(operation_1.id) , 
                    "name" : course.cid,
                    "parent": str(prereq_tuple['operation'].id),
                }
            })

        # get all edges of v
        operation_set = Operation.objects.filter(course = course)
        for operation in operation_set:
            combination_set = PreCombinationCourse.objects.filter(operation = operation)
            courses['nodes'].append({
                "data" : {
                    "id" : str(operation.id), 
                    "name" : operation.operation,
                }
            })

            courses['edges'].append({
                "data" : {
                    "id" : str(operation.id) + '-' + course.cid + "-" + str(operation_1.id),
                    "target" : course.cid + "-" + str(operation_1.id), 
                    "source": str(operation.id)
                }
            })      

            for combination in combination_set:
                q.put (
                    { 
                        "course" : combination.course,
                        "operation" : operation,
                        "level" : prereq_tuple['level'] + 1, 
                        "parent" : course,
                    }
                ) 
                # add invisble edges so that dagre javascript works to create the layout
                courses['edges'].append({
                    "data" : {
                        "target" : course.cid + "-" + str(operation_1.id), 
                        "source": combination.course.cid + "-" + str(operation.id),

                    },   
                    "classes" : 'hidden'               
                })          

    return courses
