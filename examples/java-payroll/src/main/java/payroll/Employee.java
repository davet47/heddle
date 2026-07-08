package payroll;

/** An hourly employee. Money is integer cents everywhere in this project. */
public record Employee(String id, String name, int hourlyRateCents) {}
