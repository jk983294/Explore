#!/usr/bin/perl
use warnings;

# writing template called a 'format' to output reports
# field holder
# @<<<<                     left-justified
# @>>>>                     right-justified
# @||||                     centered
# @####.##                  numeric field holder
# @*                        multiline field holder

# $name would be written as left justify within 22 character spaces and after that age will be written in two spaces
format EMPLOYEE =
===================================
@<<<<<<<<<<<<<<<<<<<<<< @<<
$name $age
@#####.##
$salary
===================================
.

format EMPLOYEE_HEADER =
===================================
Name                    Age
===================================
.

format EMPLOYEE_FOOTER =
End of Page @<
            $%
.

sub main {
    select(STDOUT);
    $~ = EMPLOYEE
      ; # associate EMPLOYEE with STDOUT, using the special variable $~ or $FORMAT_NAME
    $^ = EMPLOYEE_HEADER
      ;    # define a header and assign it to $^ or $FORMAT_TOP_NAME variable
           # define a pagination, $% or $FORMAT_PAGE_NUMBER vairable
           # set the number of lines per page, $= ( or $FORMAT_LINES_PER_PAGE )

    my @n = ( "Ali",   "Raza",  "Jaffer" );
    my @a = ( 20,      30,      40 );
    my @s = ( 2000.00, 2500.00, 4000.000 );

    my $i = 0;
    foreach (@n) {
        $name   = $_;
        $age    = $a[$i];
        $salary = $s[ $i++ ];
        write;
    }
}

main();
