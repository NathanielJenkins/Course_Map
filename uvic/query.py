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
    q.put (
        { 
            "course" : Course.objects.get(cid=cid),
            "operation" : Operation(operation="Single", id=None),
            "level" : level, 
            "parent" : Course(cid=None, id=None)
        }
    )

    while q.qsize() != 0: 
        
        prereq_tuple = q.get()
        course = prereq_tuple['course']
        operation_1 = prereq_tuple['operation']

        courses['nodes'].append({
                "data" : {
                    "id" : course.cid + "-" + str(operation_1.id) , 
                    "name" : course.cid,
                    "parent": str(prereq_tuple['operation'].id),
                    "type" : "course"
                }
            })

        # get all edges of v
        operation_set = Operation.objects.filter(course = course)
        for operation in operation_set:
            combination_set = PreCombinationCourse.objects.filter(operation = operation)
            if (operation.operation != "Single"):
                courses['nodes'].append({
                    "data" : {
                        "id" : str(operation.id), 
                        "name" : operation.operation,
                        "type" : "operation"
                    }
                })
            for combination in combination_set:
                q.put (
                    { 
                        "course" : combination.course,
                        "operation" : operation,
                        "level" : prereq_tuple['level'] + 1, 
                        "parent" : course
                    }
                ) 

                courses['edges'].append({
                    "data" : {
                        "id" : course.cid + "-" + str(operation_1.id) + "-" + combination.course.cid + "-" + str(operation.id),
                        "target" : course.cid + "-" + str(operation_1.id), 
                        "source": combination.course.cid + "-" + str(operation.id)
                    }                  
                })      
    print(courses)


    return courses
