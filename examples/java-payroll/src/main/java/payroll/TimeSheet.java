package payroll;

/** One employee's whole hours for one week; overtime accounting lives in Pay. */
public record TimeSheet(String employeeId, int hoursWorked) {}
