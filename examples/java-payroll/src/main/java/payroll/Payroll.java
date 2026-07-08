package payroll;

import java.util.List;
import java.util.Locale;

/** The payroll run: slips per employee, formatting, and run totals. */
public final class Payroll {

    private Payroll() {}

    /** The whole pipeline for one employee: gross, withholding, net, in one slip. */
    public static PaySlip slipFor(Employee employee, TimeSheet sheet) {
        int gross = Pay.grossCents(employee, sheet);
        return new PaySlip(
                employee.id(), gross, Tax.withholdingCents(gross), Tax.netCents(gross));
    }

    /** "$12.34" — dollars with exactly two cent digits; the minus sign leads. */
    public static String formatCents(int cents) {
        long abs = Math.abs((long) cents);
        return (cents < 0 ? "-$" : "$") + (abs / 100) + "."
                + String.format(Locale.ROOT, "%02d", abs % 100);
    }

    /** One line per money field, all through formatCents; ends with net pay. */
    public static String render(Employee employee, PaySlip slip) {
        return employee.name() + " (" + slip.employeeId() + ")\n"
                + "  gross " + formatCents(slip.grossCents()) + "\n"
                + "  tax   " + formatCents(slip.taxCents()) + "\n"
                + "  net   " + formatCents(slip.netCents());
    }

    /** What the run pays out in total; an empty run totals zero. */
    public static int totalNetCents(List<PaySlip> slips) {
        return slips.stream().mapToInt(PaySlip::netCents).sum();
    }
}
