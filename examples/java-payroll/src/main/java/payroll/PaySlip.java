package payroll;

/** The result of a payroll run for one employee; net is gross minus tax. */
public record PaySlip(String employeeId, int grossCents, int taxCents, int netCents) {}
