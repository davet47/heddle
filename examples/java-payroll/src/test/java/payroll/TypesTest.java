package payroll;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class TypesTest {

    @Test
    void employeeCarriesAnHourlyRateInCents() {
        Employee e = new Employee("e1", "Ada", 2000);
        assertEquals(2000, e.hourlyRateCents());
        assertEquals(new Employee("e1", "Ada", 2000), e);
    }

    @Test
    void timeSheetRecordsWholeHoursForOneWeek() {
        TimeSheet t = new TimeSheet("e1", 45);
        assertEquals("e1", t.employeeId());
        assertEquals(45, t.hoursWorked());
    }

    @Test
    void paySlipHoldsTheRunResult() {
        PaySlip s = new PaySlip("e1", 95_000, 14_000, 81_000);
        assertEquals(81_000, s.netCents());
        assertEquals(new PaySlip("e1", 95_000, 14_000, 81_000), s);
    }
}
