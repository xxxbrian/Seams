# Meeting minutes

## 26/02 Weekly meeting

**Participation:** _Steve Yang_, _Bojin Li_, _Cicy Zhou_, _Weihou Zeng_

**Minute taker:** _Steve Yang_, _Bojin Li_

**Topic:**

- Split the project into test and implementation parts.
- Make a schedule of test part. We will end this part this week.
- Give individual mission to every teammates ( 2 test functions / person ). Everyone’s mission will be given on issue board.
- Brainstorming how to test these functions.
- Clarify the rules of merging: Before merging, let at least 2 teammates know and let them test and approve the branch.
- Make issue labels and issue board. Use these labels to let teammates know the status of programing.

**About issue labels:**

_Special:_

**-** ![](https://img.shields.io/badge/label-Announcement-%23eee600) _Use this tag when you need to inform other group members._

**-** ![](https://img.shields.io/badge/label-Need%20Help-%23c21e56) _Use this label when you need other group members to help you._

_Basic:_

**-** ![](https://img.shields.io/badge/label-bug-%23d9534f) _Report a bug_

**-** ![](https://img.shields.io/badge/label-discussion-%236699cc) _Group discussion required_

**-** ![](https://img.shields.io/badge/label-documentation-%23f7e7ce) _Documentation changes required_

**-** ![](https://img.shields.io/badge/label-enhancement-%233cb371) _Functional enhancement required_

**-** ![](https://img.shields.io/badge/label-feature-%23ed9121) _New feature requested_

_Status:_

**-** ![](https://img.shields.io/badge/label-todo-%239400d3) _Add this label for tasks that have not been started_

**-** ![](https://img.shields.io/badge/label-in%20progress-%239400d3) _Add this label for tasks that have already started_

**-** ![](https://img.shields.io/badge/label-in%20test-%239400d3) _Add this label for tasks that have already started_

**-** ![](https://img.shields.io/badge/label-completed-%239400d3) _Add this label for tasks that have been approved_

## 01/03 Weekly meeting

**Participation:** _Steve Yang_, _Bojin Li_, _Cicy Zhou_, _Weihou Zeng_, _Quan Gu_

**Minute taker:** _Steve Yang_, _Bojin Li_

**Topic:**

- Discussing which situations, we should test in `auth_test`. We should follow the **black-box** rule, which means we can’t use any functions or variables not define in interface.
- When finished `auth_register` and `auth_login`, we found some bugs in our test program. According to ED forum, we know the meaning of `auth_user_id` and `u_id`, hence we change the variable name in our test program, which used `u_id` before. But we should use `auth_user_id` because it is the return value.
- Change the way to test `channel_details`. Because list is ordered, we can’t just use `==` straitly. Hence, we use the `set()` function to compare `all_members` and `owner_members`.
- Discussing a method named `to_dict`, which is really helpful when we need to return a dictionary in a function.
- Discusses the methods we need to provide in our `Class`.

## 11/03 Weekly Meeting

**Participation:** _Bojin Li_, _Cicy Zhou_, _Weihou Zeng_, _Quan Gu_

**Minute taker:** _Cicy Zhou_


