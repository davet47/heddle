package payroll;

/** Gross-pay arithmetic: regular hours at rate, overtime at time-and-a-half. */
public final class Pay {

    static final int REGULAR_HOURS = 40;

    private Pay() {}

    /** Hours past the 40-hour week; never negative. */
    public static int overtimeHours(TimeSheet sheet) {
        return Math.max(0, sheet.hoursWorked() - REGULAR_HOURS);
    }

    /** Regular hours at rate, overtime at time-and-a-half, integer-floored per term. */
    public static int grossCents(Employee employee, TimeSheet sheet) {
        int overtime = overtimeHours(sheet);
        int regular = sheet.hoursWorked() - overtime;
        return employee.hourlyRateCents() * regular
                + employee.hourlyRateCents() * 3 * overtime / 2;
    }
}
