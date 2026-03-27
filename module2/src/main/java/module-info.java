module com.example.module2 {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.module2 to javafx.fxml;
    exports com.example.module2;
}