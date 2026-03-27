/*
 * Project: Module 2 - Seat Reservation GUI Application Assignment
 * Author: Nicole Tressler
 * Auburn Email: nit0005@auburn.edu
 * Date: March 27, 2026
 * Description: This class represents a seat reservation with flight details,
 * passenger information, and baggage/service options.
 */

public class SeatReservation {

    private String flightDesignator;
    private java.time.LocalDate flightDate;
    private String firstName;
    private String lastName;
    private int numberOfBags;
    private boolean flyingWithInfant;
    private boolean flyingWithTravelInsurance;

    public String getFlightDesignator() {
        return flightDesignator;
    }

    public void setFlightDesignator(String fd) {
        if (fd == null || fd.length() < 4 || fd.length() > 6) {
            throw new IllegalArgumentException("Flight designator must be between 4 and 6 characters");
        }
        this.flightDesignator = fd;
    }

    public java.time.LocalDate getFlightDate() {
        return flightDate;
    }

    public void setFlightDate(java.time.LocalDate date) {
        flightDate = date;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String fn) {
        if (fn == null || fn.length() < 2 || fn.length() > 15) {
            throw new IllegalArgumentException("First name must be between 2 and 15 characters");
        }
        firstName = fn;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String ln) {
        if (ln == null || ln.length() < 2 || ln.length() > 15) {
            throw new IllegalArgumentException("Last name must be between 2 and 15 characters");
        }
        lastName = ln;
    }

    public int getNumberOfBags() {
        return numberOfBags;
    }

    public void setNumberOfBags(int numberOfBags) {
        this.numberOfBags = numberOfBags;
    }

    public boolean isFlyingWithInfant() {
        return flyingWithInfant;
    }

    public void makeFlyingWithInfant() {
        this.flyingWithInfant = true;
    }

    public void makeNotFlyingWithInfant() {
        this.flyingWithInfant = false;
    }

    public boolean hasTravelInsurance() {
        return flyingWithTravelInsurance;
    }

    public void makeFlyingWithTravelInsurance() {
        this.flyingWithTravelInsurance = true;
    }

    public void makeNotFlyingWithTravelInsurance() {
        this.flyingWithTravelInsurance = false;
    }

    public String toString() {
        return "SeatReservation{" +
                "flightDesignator=" + (flightDesignator == null ? "null" : flightDesignator) +
                ", flightDate=" + (flightDate == null ? "null" : flightDate) +
                ", firstName=" + (firstName == null ? "null" : firstName) +
                ", lastName=" + (lastName == null ? "null" : lastName) +
                ", numberOfBags=" + numberOfBags +
                ", flyingWithInfant=" + flyingWithInfant +
                ", flyingWithTravelInsurance=" + flyingWithTravelInsurance +
                '}';
    }
}
