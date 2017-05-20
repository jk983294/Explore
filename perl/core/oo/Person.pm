#!/usr/bin/perl
package Person;

sub new {
    my $class = shift;
    my $self = {_firstName => shift, _lastName => shift, _ssn => shift,};
    bless $self, $class;    # return a reference which ultimately becomes an object
    return $self;
}

sub setFirstName {
    my ( $self, $firstName ) = @_;
    $self->{_firstName} = $firstName if defined($firstName);
    return $self->{_firstName};
}

sub getFirstName {
    my ($self) = @_;
    return $self->{_firstName};
}
1;
