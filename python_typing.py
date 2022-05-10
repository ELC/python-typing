"""
All of the content shown here has been adapted from the official docs available
at: https://docs.python.org/3/library/typing.html

To properly follow this guide, use Visual Studio Code with the Python and
Pylance extension installed and with these two options enabled in the settings:

```json
"python.languageServer": "Pylance", 
"python.analysis.typeCheckingMode": "strict",
```

This document targets all official supported Python versions (3.7+), there are
some features only available for certain versions, when that is the case, it
will be explicitly noticed.

One example is the use of PEP 585 which is for 3.9+, however since this is a
convenience and not a functional feature, all syntax will be compatible with
3.7+.

"""


####################################################
# 1. Basic Typing
####################################################

####################################################
# 1.1 Simple Data Types
####################################################

numbers_integer: int = 10
numbers_float: float = 10.0
numbers_integer_with_float: int = 10.0  # Warning - 10.0 is not a float

name: str = "John"
name_stream: bytes = b"John"

complex_solution: complex = 2 + 4j

base_object: object = "Hello"

####################################################
# 1.2 Complex Data Types
####################################################

from typing import List, Set, Dict, Tuple


marks: List[float] = [4.2, 7.6, 2.5]
marks.append("John")  # Warning - John is not a float

students: Set[str] = {"John", "Mary", "David"}
students.add(4)  # Warning - 4 is not a str

point: Tuple[float, float] = (1.5, 2.5)
point = (0.5, 4.5)  # No Warning
point = (0.5, 4.5, 1.0)  # Warning - Tuple does not allow size changes

any_length_tuple: Tuple[float, ...] = (0.5, 4.5, 1.0)
any_length_tuple = (0.5, 4.5, 1.0, 5.0)  # No Warning
any_length_tuple = (0.5, 4.5, 1.0, "5.0")  # Warning - Type might be homogeneous

poly_line: List[Tuple[float, float]] = [(0.0, 0.0), (1.5, 1.5)]
poly_line.append((3.0, 1.5))  # No Warning
poly_line.append([4.0, 0.5])  # Warning - List is not a Tuple

students_marks: Dict[str, int] = {}
students_marks["Mary"] = 9  # No Warning
students_marks["John"] = 6.5  # Warning - 6.5 is not an int


# Explicitly typing when unpacking

first_in_tuple: float
second_in_tuple: float
first_in_tuple, second_in_tuple = (0.5, 4.5)


# Alternative syntax in Python 3.9+

point_2: tuple[float, float] = (1.5, 2.5)
poly_line_2: list[tuple[float, float]] = [(0.0, 0.0), (1.5, 1.5)]
students_marks: dict[str, int] = {}


####################################################
# 2. Classes and Inheritance
####################################################


from abc import ABC


class PaymentSystem(ABC):
    def pay(self) -> None:
        raise NotImplementedError()


class DebitPaymentSystem(PaymentSystem):
    def pay(self) -> None:
        print("You are paying with Debit")


payment: PaymentSystem = DebitPaymentSystem()  # No Warning
payment.pay()


####################################################
# 3. Automatic Type Inference
####################################################


teachers = ["Andrew", "Alex", "Jason"]  # Type inferred to be List[str]
teachers.append(7.5)  # Warning - 7.5 is not str

# Caveats Type inference on empty complex types

participants_scores = []  # Type inferred to be List but element type is not inferred
participants_scores.append(5.0)  # Warning

# Solution
participants_scores_alt: List[float] = []
participants_scores_alt.append(5.0)  # No Warning


####################################################
# 4. Functions
####################################################


def multiply(a: float, b: float) -> float:
    return a * b


multiply(4, 4)  # No Warning
multiply("a", 4)  # Warning, "a" is not a float


# Without Return -> Return None


def hello_world() -> None:
    print("Hello World")


# Function that never returns

from typing import NoReturn

def raise_exception(exception: Exception) -> NoReturn:
    print(f"{exception.__class__.__name__} was thrown!")
    raise exception

try:
    raise_exception(ValueError())
except Exception:
    pass


####################################################
# 5. Classes
####################################################

from dataclasses import dataclass


@dataclass
class Vehicle:
    speed: float
    color: str


@dataclass
class Truck(Vehicle):
    tare: float


def show_vehicle(vehicle: Vehicle):  # Classes can be used in functions
    print(f"This vehicle can go to {vehicle.speed} and is {vehicle.color}")


def show_truck(truck: Truck):
    print(f"This truck can go to {truck.speed} and is {truck.color}")


new_vehicle = Vehicle(speed=140, color="Blue")
new_truck = Truck(speed=90, color="Red", tare=10)
show_vehicle(new_vehicle)  # No Warnings
show_vehicle(new_truck)  # A function can take subclass of the type hint as well
show_truck(new_truck)  # No warnings
show_truck(new_vehicle)  # Warning - Super classes cannot be passed


####################################################
# 6. TypeAliases
####################################################


Point2D = Tuple[float, float]
Triangle = Tuple[Point2D, Point2D, Point2D]

poligon: Triangle = ((0.0, 0.0), (0.0, 1.0), (1.0, 1.0))


# Splicitly typing aliases

from typing import TypeAlias  # Requires Python 3.10+

# from typing_extensions import TypeAlias

Pentagon: TypeAlias = Tuple[Point2D, Point2D, Point2D, Point2D, Point2D]

house_polygon: Pentagon = (
    (0.0, 0.0),
    (4.0, 0.0),
    (4.0, 4.0),
    (2.0, 6.0),
    (0.0, 4.0),
)


####################################################
# 7. NewType
####################################################


from typing import NewType

UserID = NewType("UserID", int)

user_a = UserID(156)
user_b = UserID(654)

assert isinstance(user_a, int)  # Passes
assert user_a + user_b == 156 + 654  # Normal int operations

sum_of_ids = user_a + user_b

assert isinstance(sum_of_ids, int)  # Passes


def is_user_valid(user_id: UserID):
    return f"Welcome {user_id}!"


is_user_valid(user_a)  # No Warning
is_user_valid(user_a + user_b)  # Warning - Operation on NewType returns supertype
is_user_valid(156)  # Warning - 156 is not UserID


####################################################
# 8. TypedDict
####################################################

####################################################
# 8.1 Functional Syntax
####################################################

# Specifying specific keys in a dictionary

from typing import TypedDict  # Requires Python 3.8+

# from typing_extensions import TypedDict

# As TypeAlias
ProductDict = TypedDict("Product", name=str, price=float)

mobile_x: ProductDict = {"name": "MobileX", "price": 300}
mobile_x["price"] = 350  # No Warning
mobile_x["brand"] = "XCo"  # Warning - brand is not a defined key

mobile_y: ProductDict = {"name": "MobileY"}  # Warning, all keys are expected by default


####################################################
# 8.2 Class Syntax
####################################################

# All keys must be valid identifiers

class ProductClass(TypedDict):
    name: str
    price: float


mobile_x_alt: ProductClass = {"name": "MobileX", "price": 300}
mobile_x_alt["price"] = 350  # No Warning
mobile_x_alt["brand"] = "XCo"  # Warning - brand is not a defined key


# Allowing for optional keys - Only with class syntax

class UnpricedProduct(TypedDict, total=False):
    name: str
    price: float

mobile_z: UnpricedProduct = {"name": "MobileZ"}  # No Warning


# Inheritance

class Person(TypedDict):
    name: str
    age: float


class Student(Person, total=False):
    mark: float


teacher: Person = {"name": "Alfred", "age": 30}  # No Warning
teacher["mark"] = 0  # Warning - Person has no key mark

student: Student = {"name": "Peter", "age": 16}  # No Warning
student["mark"] = 6.5  # No Warning


####################################################
# 9. Special Data Types
####################################################


####################################################
# 9.1 Final
####################################################


# Avoid overwriting

from typing import Final  # Requires Python 3.8+

# from typing_extensions import Final

origin: Final[Tuple[float, float]] = (0.0, 0.0)
origin = (1.5, 1.5)  # Warning

FREE_FALL_ACCELERATION: Final[float] = 9.764  # Usefor for constants


# Application in OOP

from dataclasses import dataclass

from typing import final  # Requires Python 3.8+

# from typing_extensions import final


@dataclass
class Citizen:
    name: str
    tax_id: Final[int]

    @final
    def get_summary(self):
        return f"Citizen data: {self.name} - {self.tax_id}"


@dataclass
class Diplomat(Citizen):
    country: str

    def get_summary(self):  # Warning
        return f"This diplomat represents {self.country}"


citizen = Citizen("John", 1235)
citizen.name = "John White"  # No Warning
citizen.tax_id = 654  # Warning Tax ID is Final
citizen.get_summary()  # No Warning

diplomat = Diplomat("John", 1235, "Pythonland")
citizen.get_summary()  # No Warning - See Warning in declaration


####################################################
# 9.2 Literal
####################################################


# Specifying subset of possible values

from typing import Literal  # Requires Python 3.8+

# from typing_extensions import Literal

sex: Literal["M", "F"] = "F"
sex = "M"
sex = "Masculine"  # Warning


####################################################
# 9.3 Any
####################################################

from typing import Any

# When Types are unknown - NOT RECOMMENDED

parameter: Dict[str, Any] = {}
parameter["workers"] = 5
parameter["experiment_name"] = "attemp_01"
parameter["config"] = {"id": 123, "module": "Testing"}

# Try avoid using Any whenver possible, in the previous example, use TypedDict
# instead

####################################################
# 9.3 ClassVar
####################################################

from typing import ClassVar


class Car:
    petrol_price: ClassVar[float] = 2

    def set_pretol_price(self, value: float):
        self.petrol_price = value  # Warning


new_car = Car()
assert Car.petrol_price == 2  # Passes - Checks class variable
assert new_car.petrol_price == 2  # Passes - Checks class variable
new_car.set_pretol_price(5)  # Sets instance variable that shadows class variable
assert Car.petrol_price == 2  # Passes - Class variable is intact
assert new_car.petrol_price == 5  # Passes - Access instance variable


# Works with dataclasses

from dataclasses import dataclass

@dataclass
class Motorbike:
    brand: str
    speed: float
    maintenance_frequency: ClassVar[float]


####################################################
# 10. Union
####################################################

from typing import Union


def double(number: Union[float, List[float]]) -> Union[float, List[float]]:
    if isinstance(number, list):
        return [x * 2 for x in number]
    return number * 2

result: float = double(4)  # Warning
result_2: Union[float, List[float]] = double(4)  # No Warning


# Alternative Syntax

FloatOrList = float | List[float]  # Requires Python 3.10+


def double_alternative(number: FloatOrList) -> FloatOrList:
    if isinstance(number, list):
        return [x * 2 for x in number]
    return number * 2


result_alternative: float = double_alternative(4)  # Warning
result_alternative_2: FloatOrList = double_alternative(4)  # No Warning


# Special case - None

user_input: Union[str, None] = "Admin"

def greetings(name: Union[str, None]) -> None:
    if name is None:
        print("No name")
    print(f"Welcome {name}.")

greetings(user_input)  # No Warning


####################################################
# 11. Optional
####################################################


from typing import Optional

user_input_alternative: Optional[str] = "Admin"

def greetings_alternative(name: Optional[str]) -> None:
    if name is None:
        print("No name")
    print(f"Welcome {name}.")


greetings_alternative(user_input_alternative)  # No Warning


####################################################
# 12. Automatic Narrowing
####################################################


def get_scores() -> Union[float, List[float]]:
    return [4.5, 0.6]


field: Union[float, List[float]] = get_scores()

field.append(6.2)  # Warning, type might be float and float has no append

if isinstance(field, list):
    field.append(6.2)  # No Warning - The type is narrowed to list


####################################################
# 13. Custom Narrowing
####################################################


from typing import TypeGuard  # Requires Python 3.10+

# from typing_extensions import TypeGuard


def convertable_to_string(value: List[Any]) -> TypeGuard[List[str]]:
    return all(isinstance(x, str) for x in value)


data: List[object] = ["5", "8", "1", "0", "6"]

join_object = " ".join(data)  # Warning - Object is not compatible with join

if convertable_to_string(data):
    join_str = " ".join(data)  # No Warning


####################################################
# 14. Overloads
####################################################


from typing import overload


@overload
def triple(number: float) -> float:
    ...


@overload
def triple(number: List[float]) -> List[float]:
    ...


def triple(number: Union[float, List[float]]) -> Union[float, List[float]]:
    if isinstance(number, list):
        return [x * 3 for x in number]
    return number * 3


triple_result: float = triple(4)  # No Warning
triple_result_2: List[float] = triple([4])  # No Warning
triple_result_3: Union[float, List[float]] = triple(4)  # No Warning
triple_result_4: Union[float, List[float]] = triple([4])  # No Warning


####################################################
# 15.1 Protocols
####################################################

####################################################
# 15.2 Built-in Protocols
####################################################


# Typical use case:


def sum_all_elements(values: List[float]) -> float:
    return sum(values)


sum_all_elements([1, 2, 3])  # No Warning
sum_all_elements((1, 2, 3))  # Warning - Tuple is not List


# Potential fix:


def sum_all_elements_2(values: Union[List[float], Tuple[float, ...]]) -> float:
    return sum(values)


sum_all_elements_2([1, 2, 3])  # No Warning
sum_all_elements_2((1, 2, 3))  # No Warning
sum_all_elements_2(range(1, 4))  # Warning - range is neither Tuple nor List


# Using Built-In Protocols

# Reference: https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes

from typing import Iterable  # See https://peps.python.org/pep-0585/


def sum_all_elements_2(values: Iterable[float]) -> float:
    return sum(values)


sum_all_elements_2([1, 2, 3])  # No Warning
sum_all_elements_2((1, 2, 3))  # No Warning
sum_all_elements_2(range(1, 4))  # No Warning


####################################################
# 15.2 Custom Protocols
####################################################


from typing import Protocol  # Requires Python 3.8+

# from typing_extensions import Protocol


class StreamingSystem(Protocol):
    def play(self) -> None:
        ...


class WebStreamingSystem:  # Note: no inheritance needed
    def play(self) -> None:
        print("You are playing from the website")


streaming: StreamingSystem = WebStreamingSystem()  # No Warning


####################################################
# 16. Typing Functions
####################################################

####################################################
# 16.1 Callable
####################################################


from typing import Callable


def map_function(
    function: Callable[[float], float], elements: List[float]
) -> List[float]:
    return [function(element) for element in elements]


def double_def(x: float):
    return x * 2


class Doubler:
    def __call__(self, value: float) -> float:
        return value * 2


numbers = [1.5, 0.5, 3.5, 4.0]

map_function(double_def, numbers)  # No Warning
map_function(lambda x: x * 2, numbers)  # No Warning
map_function(Doubler(), numbers)  # No Warning


####################################################
# 16.2 Args and Kwargs
####################################################


def summation(*args: float, **kwargs: float) -> float:
    return sum(args) + sum(kwargs.values())


assert summation(2, x=4) == 6  # No Warning


####################################################
# 16.3 Closures
####################################################


def multiply(x: float) -> Callable[[float], float]:
    def helper(y: float) -> float:
        return x * y

    return helper


assert multiply(2)(3) == 6  # No Warning


####################################################
# 17. TypeVar and Generics
####################################################


####################################################
# 17.1 Unbound and Unconstrained
####################################################

from dataclasses import dataclass

# Problem

from typing import Union, Sequence

FloatStrUnion = Union[float, str]


def first_union(values: List[FloatStrUnion]) -> FloatStrUnion:
    return values[0]


test_float: float
test_str: str
test_union: FloatStrUnion

test_float = first_union([1, 2, 3])  # Warning - Int is not Union
test_float = first_union([1.5, 2.5, 3.5])  # Warning - Float is not Union
test_str = first_union(["1.5", "2.5", "3.5"])  # Warning - Str is not Union
test_union = first_union([1.5, "2.5"])  # No Warning - Union is expected


# Initial Solution

from typing import TypeVar

T = TypeVar("T")


def first_typevar(values: Sequence[T]) -> T:
    return values[0]


test_float = first_typevar([1, 2, 3])  # No Warning - Infered type is int
test_float = first_typevar([1.5, 2.5, 3.5])  # No Warning - Infered type is float
test_str = first_typevar(["1.5", "2.5", "3.5"])  # No Warning - Infered type is str
test_union = first_typevar([1.5, "2.5"])  # No Warning - Infered type is Union[str, int]


####################################################
# 17.1 Constrained TypeVars
####################################################


FloatOrString = TypeVar("FloatOrString", float, str)


def first_typevar_constrained(values: List[FloatOrString]) -> FloatOrString:
    return values[0]


test_float = first_typevar_constrained([1, 2, 3])  # No Warning - Infered type is int
test_float = first_typevar_constrained(
    [1.5, 2.5, 3.5]
)  # No Warning - Infered type is float
test_str = first_typevar_constrained(
    ["1.5", "2.5", "3.5"]
)  # No Warning - Infered type is str
test_union = first_typevar_constrained(
    [1.5, "2.5"]
)  # No Warning - Union is incompatible with given constraints


####################################################
# 17.1 Bounded TypeVars
####################################################


BoundedFloat = TypeVar("BoundedFloat", bound=float)


def first_typevar_bounded(values: List[BoundedFloat]) -> BoundedFloat:
    return values[0]


test_float = first_typevar_bounded([1, 2, 3])  # No Warning - Infered type is int
test_float = first_typevar_bounded(
    [1.5, 2.5, 3.5]
)  # No Warning - Infered type is float
test_str = first_typevar_bounded(
    ["1.5", "2.5", "3.5"]
)  # No Warning - Infered type is str
test_union = first_typevar_bounded(
    [1.5, "2.5"]
)  # No Warning - Union is incompatible with given constraints


####################################################
# 17.1 Covariant vs Contravariant vs Invariant
####################################################

# By default some types are invariant, meaning that even if an object is a
# subclass of the defined in the type hint, there will be warnings.


from abc import ABC

@dataclass
class AbstractStreamingServiceConfig(ABC):
    ...


StreamConfig = TypeVar("StreamConfig", bound=AbstractStreamingServiceConfig)


@dataclass
class AbstractStreamingService(ABC, Generic[StreamConfig]):
    config: StreamConfig
    ...


@dataclass
class WebCamStreamingServiceConfig(AbstractStreamingServiceConfig):
    quality: str = "720p"
    ...


@dataclass
class HighSpeedWebCamStreamingServiceConfig(WebCamStreamingServiceConfig):
    fps: int = 15000
    ...


@dataclass
class WebCamStreamingService(AbstractStreamingService[WebCamStreamingServiceConfig]):
    def show_quality(self) -> str:
        return self.config.quality  # No Warning


WebCamStreamingService(AbstractStreamingServiceConfig())  # Warning
WebCamStreamingService(WebCamStreamingServiceConfig())  # No Warning
WebCamStreamingService(HighSpeedWebCamStreamingServiceConfig())  # No Warning


####################################################
# 18. ParamSpec & Concatenate
####################################################


####################################################
# 19. Generics
####################################################


####################################################
# 20. Other Features
####################################################

####################################################
# 20.1 Annotated
####################################################
