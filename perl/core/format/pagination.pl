#!/usr/bin/perl
use warnings;

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
Name                    Age Page @<
                                 $%
===================================
.

sub main {
    select(STDOUT);
    $~ = EMPLOYEE
      ; # associate EMPLOYEE with STDOUT, using the special variable $~ or $FORMAT_NAME
    $^ = EMPLOYEE_HEADER
      ;    # define a header and assign it to $^ or $FORMAT_TOP_NAME variable
           # define a pagination, $% or $FORMAT_PAGE_NUMBER vairable in format
           # set the number of lines per page, $= ( or $FORMAT_LINES_PER_PAGE )

    @n = ( "Ali",   "Raza",  "Jaffer" );
    @a = ( 20,      30,      40 );
    @s = ( 2000.00, 2500.00, 4000.000 );

    $i = 0;
    foreach (@n) {
        $name   = $_;
        $age    = $a[$i];
        $salary = $s[ $i++ ];
        write;
    }
}

main();
