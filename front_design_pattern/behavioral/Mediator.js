/**
 * A Mediator is an object that coordinates interactions
 * (logic and behavior) between multiple objects.
 * It makes decisions on when to call which objects,
 * based on the actions (or inaction) of other objects and input.
 */
var mediator = {};

var orgChart = {

    addNewEmployee: function(){

        // getEmployeeDetail provides a view that users interact with
        var employeeDetail = this.getEmployeeDetail();

        // when the employee detail is complete, the mediator (the 'orgchart' object)
        // decides what should happen next
        employeeDetail.on("complete", function(employee){

            // set up additional objects that have additional events, which are used
            // by the mediator to do additional things
            var managerSelector = this.selectManager(employee);
            managerSelector.on("save", function(employee){
                employee.save();
            });

        });
    },

    deleteEmployee : function(){
        //...
    }
    // ...
}