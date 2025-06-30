cons_cpu_deq_cnt_range -> 
cons_cpu_cap_cnt_range -> 
cons_cpu_valid_cnt_range -> 
cons_cpu_valid_cnt_equation_at_time0 -> 
cons_cpu_valid_cnt_equation_at_time1 -> 
cons_cpu_valid_cnt_equation_at_time2 -> 
cons_cpu_cap_cnt_equation -> 
cons_init_source_cpu -> 
 And(And(cpu_cap_cnt_at_time_0 == 7,
        And(cpu_input_cnt_at_time_0 >= 0,
            cpu_input_cnt_at_time_0 <= cpu_cap_cnt_at_time_0),
        And(cpu_input_cnt_at_time_1 >= 0,
            cpu_input_cnt_at_time_1 <= cpu_cap_cnt_at_time_1),
        And(cpu_input_cnt_at_time_2 >= 0,
            cpu_input_cnt_at_time_2 <= cpu_cap_cnt_at_time_2),
        And(cpu_input_cnt_at_time_3 >= 0,
            cpu_input_cnt_at_time_3 <= cpu_cap_cnt_at_time_3),
        And(cpu_input_cnt_at_time_4 >= 0,
            cpu_input_cnt_at_time_4 <= cpu_cap_cnt_at_time_4),
        And(cpu_input_cnt_at_time_5 >= 0,
            cpu_input_cnt_at_time_5 <= cpu_cap_cnt_at_time_5)),
    cpu_credit_cnt_at_time_0 == 7,
    And(cpu_input_cnt_at_time_0 >= 0,
        cpu_input_cnt_at_time_0 <= cpu_credit_cnt_at_time_0),
    And(cpu_input_cnt_at_time_1 >= 0,
        cpu_input_cnt_at_time_1 <= cpu_credit_cnt_at_time_1),
    And(cpu_input_cnt_at_time_2 >= 0,
        cpu_input_cnt_at_time_2 <= cpu_credit_cnt_at_time_2),
    And(cpu_input_cnt_at_time_3 >= 0,
        cpu_input_cnt_at_time_3 <= cpu_credit_cnt_at_time_3),
    And(cpu_input_cnt_at_time_4 >= 0,
        cpu_input_cnt_at_time_4 <= cpu_credit_cnt_at_time_4),
    And(cpu_input_cnt_at_time_5 >= 0,
        cpu_input_cnt_at_time_5 <= cpu_credit_cnt_at_time_5))
cons_cha_valid_cnt_equation_at_time1 -> 
cons_cha_valid_cnt_equation_at_time2 -> 
cons_cha_valid_cnt_equation_at_time3 -> 
cons_cha_cap_cnt_equation -> 
cons_cha_sd_deq_cnt_range -> 
cons_cha_sd_cap_cnt_range -> 
cons_cha_sd_valid_cnt_range -> 
cons_cha_sd_deq_must_less_valid_cnt -> 
 And(cha_sd_val_cnt_at_time_0 >= cha_sd_deq_cnt_at_time_0,
    cha_sd_val_cnt_at_time_1 >= cha_sd_deq_cnt_at_time_1,
    cha_sd_val_cnt_at_time_2 >= cha_sd_deq_cnt_at_time_2,
    cha_sd_val_cnt_at_time_3 >= cha_sd_deq_cnt_at_time_3,
    cha_sd_val_cnt_at_time_4 >= cha_sd_deq_cnt_at_time_4,
    cha_sd_val_cnt_at_time_5 >= cha_sd_deq_cnt_at_time_5)
cons_cha_sd_valid_cnt_equation_at_time1 -> 
cons_cha_sd_valid_cnt_equation_at_time2 -> 
cons_cha_sd_valid_cnt_equation_at_time3 -> 
cons_cha_sd_cap_cnt_equation -> 
cons_init_non_source_cha_sd -> 
 And(cha_sd_deq_cnt_at_time_0 == 0,
    cha_sd_val_cnt_at_time_0 == 0,
    cha_sd_cap_cnt_at_time_0 == 6,
    Not(cha_sd_index_0_time_0_val),
    Not(cha_sd_index_1_time_0_val),
    Not(cha_sd_index_2_time_0_val),
    Not(cha_sd_index_3_time_0_val),
    Not(cha_sd_index_4_time_0_val),
    Not(cha_sd_index_5_time_0_val))
cons_init_non_source_cha_*1 -> 
 And(Not(cha_hit_index_0_at_time_0),
    Not(cha_hit_index_1_at_time_0),
    Not(cha_hit_index_2_at_time_0),
    Not(cha_hit_index_3_at_time_0),
    Not(cha_hit_index_4_at_time_0),
    Not(cha_hit_index_5_at_time_0))
cons_mc_deq_cnt_range -> 
cons_mc_cap_cnt_range -> 
cons_mc_valid_cnt_range -> 
cons_mc_deq_must_less_valid_cnt -> 
 And(mc_val_cnt_at_time_0 >= mc_deq_cnt_at_time_0,
    mc_val_cnt_at_time_1 >= mc_deq_cnt_at_time_1,
    mc_val_cnt_at_time_2 >= mc_deq_cnt_at_time_2,
    mc_val_cnt_at_time_3 >= mc_deq_cnt_at_time_3,
    mc_val_cnt_at_time_4 >= mc_deq_cnt_at_time_4,
    mc_val_cnt_at_time_5 >= mc_deq_cnt_at_time_5)
cons_mc_valid_cnt_equation_at_time1 -> 
cons_mc_valid_cnt_equation_at_time2 -> 
cons_mc_valid_cnt_equation_at_time3 -> 
cons_mc_valid_cnt_equation_at_time4 -> 
cons_mc_cap_cnt_equation -> 
cons_init_non_source_mc -> 
 And(mc_deq_cnt_at_time_0 == 0,
    mc_val_cnt_at_time_0 == 0,
    mc_cap_cnt_at_time_0 == 5,
    Not(mc_index_0_time_0_val),
    Not(mc_index_1_time_0_val),
    Not(mc_index_2_time_0_val),
    Not(mc_index_3_time_0_val),
    Not(mc_index_4_time_0_val))
cons_fifo_condition3_for_mc_index_0_at_time_1 -> 
 Implies(And(5 - mc_cap_cnt_at_time_1 +
            cha_sd_deq_cnt_at_time_0 <
            1,
            True),
        Not(mc_index_0_time_1_val))
cons_fifo_condition3_for_mc_index_1_at_time_1 -> 
 Implies(And(5 - mc_cap_cnt_at_time_1 +
            cha_sd_deq_cnt_at_time_0 <
            2,
            True),
        Not(mc_index_1_time_1_val))
cons_fifo_condition3_for_mc_index_2_at_time_1 -> 
 Implies(And(5 - mc_cap_cnt_at_time_1 +
            cha_sd_deq_cnt_at_time_0 <
            3,
            True),
        Not(mc_index_2_time_1_val))
cons_fifo_condition3_for_mc_index_3_at_time_1 -> 
 Implies(And(5 - mc_cap_cnt_at_time_1 +
            cha_sd_deq_cnt_at_time_0 <
            4,
            True),
        Not(mc_index_3_time_1_val))
cons_fifo_condition3_for_mc_index_4_at_time_1 -> 
 Implies(And(5 - mc_cap_cnt_at_time_1 +
            cha_sd_deq_cnt_at_time_0 <
            5,
            True),
        Not(mc_index_4_time_1_val))
cons_fifo_add_dequeue_for_cha_sd_at_time_2 -> 
 If(mc_cap_cnt_at_time_2 - cha_sd_val_cnt_at_time_1 < 0,
   cha_sd_deq_cnt_at_time_1 == mc_cap_cnt_at_time_2,
   cha_sd_deq_cnt_at_time_1 == cha_sd_val_cnt_at_time_1)
cons_fifo_condition2_for_mc_index_1_remain_0_at_time_2 -> 
 Implies(And(5 - mc_cap_cnt_at_time_2 == 0,
            5 - mc_cap_cnt_at_time_2 < 1,
            5 - mc_cap_cnt_at_time_2 +
            cha_sd_deq_cnt_at_time_1 >=
            1),
        And(cha_sd_index_0_time_1_val ==
            mc_index_0_time_2_val,
            cha_sd_index_0_time_1_src ==
            mc_index_0_time_2_src,
            cha_sd_index_0_time_1_loc ==
            mc_index_0_time_2_loc,
            cha_sd_index_0_time_1_stime ==
            mc_index_0_time_2_stime))
cons_fifo_condition2_for_mc_index_2_remain_0_at_time_2 -> 
 Implies(And(5 - mc_cap_cnt_at_time_2 == 0,
            5 - mc_cap_cnt_at_time_2 < 2,
            5 - mc_cap_cnt_at_time_2 +
            cha_sd_deq_cnt_at_time_1 >=
            2),
        And(cha_sd_index_1_time_1_val ==
            mc_index_1_time_2_val,
            cha_sd_index_1_time_1_src ==
            mc_index_1_time_2_src,
            cha_sd_index_1_time_1_loc ==
            mc_index_1_time_2_loc,
            cha_sd_index_1_time_1_stime ==
            mc_index_1_time_2_stime))
cons_fifo_condition2_for_mc_index_3_remain_0_at_time_2 -> 
 Implies(And(5 - mc_cap_cnt_at_time_2 == 0,
            5 - mc_cap_cnt_at_time_2 < 3,
            5 - mc_cap_cnt_at_time_2 +
            cha_sd_deq_cnt_at_time_1 >=
            3),
        And(cha_sd_index_2_time_1_val ==
            mc_index_2_time_2_val,
            cha_sd_index_2_time_1_src ==
            mc_index_2_time_2_src,
            cha_sd_index_2_time_1_loc ==
            mc_index_2_time_2_loc,
            cha_sd_index_2_time_1_stime ==
            mc_index_2_time_2_stime))
cons_fifo_condition2_for_mc_index_4_remain_0_at_time_2 -> 
 Implies(And(5 - mc_cap_cnt_at_time_2 == 0,
            5 - mc_cap_cnt_at_time_2 < 4,
            5 - mc_cap_cnt_at_time_2 +
            cha_sd_deq_cnt_at_time_1 >=
            4),
        And(cha_sd_index_3_time_1_val ==
            mc_index_3_time_2_val,
            cha_sd_index_3_time_1_src ==
            mc_index_3_time_2_src,
            cha_sd_index_3_time_1_loc ==
            mc_index_3_time_2_loc,
            cha_sd_index_3_time_1_stime ==
            mc_index_3_time_2_stime))
cons_fifo_condition2_for_mc_index_5_remain_0_at_time_2 -> 
 Implies(And(5 - mc_cap_cnt_at_time_2 == 0,
            5 - mc_cap_cnt_at_time_2 < 5,
            5 - mc_cap_cnt_at_time_2 +
            cha_sd_deq_cnt_at_time_1 >=
            5),
        And(cha_sd_index_4_time_1_val ==
            mc_index_4_time_2_val,
            cha_sd_index_4_time_1_src ==
            mc_index_4_time_2_src,
            cha_sd_index_4_time_1_loc ==
            mc_index_4_time_2_loc,
            cha_sd_index_4_time_1_stime ==
            mc_index_4_time_2_stime))
cons_fifo_add_dequeue_for_cha_sd_at_time_3 -> 
 If(mc_cap_cnt_at_time_3 - cha_sd_val_cnt_at_time_2 < 0,
   cha_sd_deq_cnt_at_time_2 == mc_cap_cnt_at_time_3,
   cha_sd_deq_cnt_at_time_2 == cha_sd_val_cnt_at_time_2)
cons_fifo_condition1_for_mc_index_1_deq_4_at_time_3 -> 
 Implies(And(mc_deq_cnt_at_time_2 == 4,
            5 - mc_cap_cnt_at_time_3 >= 1),
        And(mc_index_4_time_2_val == mc_index_0_time_3_val,
            mc_index_4_time_2_src == mc_index_0_time_3_src,
            mc_index_4_time_2_loc == mc_index_0_time_3_loc,
            mc_index_4_time_2_stime ==
            mc_index_0_time_3_stime))
cons_fifo_condition2_for_mc_index_2_remain_1_at_time_3 -> 
 Implies(And(5 - mc_cap_cnt_at_time_3 == 1,
            5 - mc_cap_cnt_at_time_3 < 2,
            5 - mc_cap_cnt_at_time_3 +
            cha_sd_deq_cnt_at_time_2 >=
            2),
        And(cha_sd_index_0_time_2_val ==
            mc_index_1_time_3_val,
            cha_sd_index_0_time_2_src ==
            mc_index_1_time_3_src,
            cha_sd_index_0_time_2_loc ==
            mc_index_1_time_3_loc,
            cha_sd_index_0_time_2_stime ==
            mc_index_1_time_3_stime))
cons_fifo_condition2_for_mc_index_3_remain_1_at_time_3 -> 
 Implies(And(5 - mc_cap_cnt_at_time_3 == 1,
            5 - mc_cap_cnt_at_time_3 < 3,
            5 - mc_cap_cnt_at_time_3 +
            cha_sd_deq_cnt_at_time_2 >=
            3),
        And(cha_sd_index_1_time_2_val ==
            mc_index_2_time_3_val,
            cha_sd_index_1_time_2_src ==
            mc_index_2_time_3_src,
            cha_sd_index_1_time_2_loc ==
            mc_index_2_time_3_loc,
            cha_sd_index_1_time_2_stime ==
            mc_index_2_time_3_stime))
cons_fifo_condition3_for_mc_index_3_at_time_3 -> 
 Implies(And(5 - mc_cap_cnt_at_time_3 +
            cha_sd_deq_cnt_at_time_2 <
            4,
            True),
        Not(mc_index_3_time_3_val))
cons_fifo_condition3_for_mc_index_4_at_time_3 -> 
 Implies(And(5 - mc_cap_cnt_at_time_3 +
            cha_sd_deq_cnt_at_time_2 <
            5,
            True),
        Not(mc_index_4_time_3_val))
cons_fifo_condition3_for_mc_index_0_at_time_4 -> 
 Implies(And(5 - mc_cap_cnt_at_time_4 +
            cha_sd_deq_cnt_at_time_3 <
            1,
            True),
        Not(mc_index_0_time_4_val))
cons_fifo_condition3_for_mc_index_1_at_time_4 -> 
 Implies(And(5 - mc_cap_cnt_at_time_4 +
            cha_sd_deq_cnt_at_time_3 <
            2,
            True),
        Not(mc_index_1_time_4_val))
cons_fifo_condition3_for_mc_index_2_at_time_4 -> 
 Implies(And(5 - mc_cap_cnt_at_time_4 +
            cha_sd_deq_cnt_at_time_3 <
            3,
            True),
        Not(mc_index_2_time_4_val))
cons_fifo_condition3_for_mc_index_3_at_time_4 -> 
 Implies(And(5 - mc_cap_cnt_at_time_4 +
            cha_sd_deq_cnt_at_time_3 <
            4,
            True),
        Not(mc_index_3_time_4_val))
cons_fifo_condition3_for_mc_index_4_at_time_4 -> 
 Implies(And(5 - mc_cap_cnt_at_time_4 +
            cha_sd_deq_cnt_at_time_3 <
            5,
            True),
        Not(mc_index_4_time_4_val))
cons_fifo_add_dequeue_for_cpu_at_time_1 -> 
 If(cha_cap_cnt_at_time_1 - cpu_val_cnt_at_time_0 < 0,
   cpu_deq_cnt_at_time_0 == cha_cap_cnt_at_time_1,
   cpu_deq_cnt_at_time_0 == cpu_val_cnt_at_time_0)
cons_fifo_condition2_for_cha_index_1_remain_0_at_time_1 -> 
 Implies(And(True, True, 0 + cpu_deq_cnt_at_time_0 >= 1),
        And(cpu_index_0_time_0_val == cha_index_0_time_1_val,
            cpu_index_0_time_0_src == cha_index_0_time_1_src,
            cpu_index_0_time_0_loc == cha_index_0_time_1_loc,
            cpu_index_0_time_0_stime ==
            cha_index_0_time_1_stime))
cons_fifo_condition2_for_cha_index_2_remain_0_at_time_1 -> 
 Implies(And(True, True, 0 + cpu_deq_cnt_at_time_0 >= 2),
        And(cpu_index_1_time_0_val == cha_index_1_time_1_val,
            cpu_index_1_time_0_src == cha_index_1_time_1_src,
            cpu_index_1_time_0_loc == cha_index_1_time_1_loc,
            cpu_index_1_time_0_stime ==
            cha_index_1_time_1_stime))
cons_fifo_condition2_for_cha_index_3_remain_0_at_time_1 -> 
 Implies(And(True, True, 0 + cpu_deq_cnt_at_time_0 >= 3),
        And(cpu_index_2_time_0_val == cha_index_2_time_1_val,
            cpu_index_2_time_0_src == cha_index_2_time_1_src,
            cpu_index_2_time_0_loc == cha_index_2_time_1_loc,
            cpu_index_2_time_0_stime ==
            cha_index_2_time_1_stime))
cons_fifo_condition2_for_cha_index_4_remain_0_at_time_1 -> 
 Implies(And(True, True, 0 + cpu_deq_cnt_at_time_0 >= 4),
        And(cpu_index_3_time_0_val == cha_index_3_time_1_val,
            cpu_index_3_time_0_src == cha_index_3_time_1_src,
            cpu_index_3_time_0_loc == cha_index_3_time_1_loc,
            cpu_index_3_time_0_stime ==
            cha_index_3_time_1_stime))
cons_fifo_condition2_for_cha_index_5_remain_0_at_time_1 -> 
 Implies(And(True, True, 0 + cpu_deq_cnt_at_time_0 >= 5),
        And(cpu_index_4_time_0_val == cha_index_4_time_1_val,
            cpu_index_4_time_0_src == cha_index_4_time_1_src,
            cpu_index_4_time_0_loc == cha_index_4_time_1_loc,
            cpu_index_4_time_0_stime ==
            cha_index_4_time_1_stime))
cons_fifo_condition2_for_cha_index_6_remain_0_at_time_1 -> 
 Implies(And(True, True, 0 + cpu_deq_cnt_at_time_0 >= 6),
        And(cpu_index_5_time_0_val == cha_index_5_time_1_val,
            cpu_index_5_time_0_src == cha_index_5_time_1_src,
            cpu_index_5_time_0_loc == cha_index_5_time_1_loc,
            cpu_index_5_time_0_stime ==
            cha_index_5_time_1_stime))
cons_fifo_add_dequeue_for_cpu_at_time_2 -> 
 If(cha_cap_cnt_at_time_2 - cpu_val_cnt_at_time_1 < 0,
   cpu_deq_cnt_at_time_1 == cha_cap_cnt_at_time_2,
   cpu_deq_cnt_at_time_1 == cpu_val_cnt_at_time_1)
cons_fifo_condition2_for_cha_index_1_remain_0_at_time_2 -> 
 Implies(And(True, True, 0 + cpu_deq_cnt_at_time_1 >= 1),
        And(cpu_index_0_time_1_val == cha_index_0_time_2_val,
            cpu_index_0_time_1_src == cha_index_0_time_2_src,
            cpu_index_0_time_1_loc == cha_index_0_time_2_loc,
            cpu_index_0_time_1_stime ==
            cha_index_0_time_2_stime))
cons_fifo_condition3_for_cha_index_1_at_time_2 -> 
 Implies(And(0 + cpu_deq_cnt_at_time_1 < 2, True),
        Not(cha_index_1_time_2_val))
cons_fifo_condition3_for_cha_index_2_at_time_2 -> 
 Implies(And(0 + cpu_deq_cnt_at_time_1 < 3, True),
        Not(cha_index_2_time_2_val))
cons_fifo_condition3_for_cha_index_3_at_time_2 -> 
 Implies(And(0 + cpu_deq_cnt_at_time_1 < 4, True),
        Not(cha_index_3_time_2_val))
cons_fifo_condition3_for_cha_index_4_at_time_2 -> 
 Implies(And(0 + cpu_deq_cnt_at_time_1 < 5, True),
        Not(cha_index_4_time_2_val))
cons_fifo_condition3_for_cha_index_5_at_time_2 -> 
 Implies(And(0 + cpu_deq_cnt_at_time_1 < 6, True),
        Not(cha_index_5_time_2_val))
cons_fifo_condition3_for_cha_index_0_at_time_3 -> 
 Implies(And(0 + cpu_deq_cnt_at_time_2 < 1, True),
        Not(cha_index_0_time_3_val))
cons_fifo_condition3_for_cha_index_1_at_time_3 -> 
 Implies(And(0 + cpu_deq_cnt_at_time_2 < 2, True),
        Not(cha_index_1_time_3_val))
cons_fifo_condition3_for_cha_index_2_at_time_3 -> 
 Implies(And(0 + cpu_deq_cnt_at_time_2 < 3, True),
        Not(cha_index_2_time_3_val))
cons_fifo_condition3_for_cha_index_3_at_time_3 -> 
 Implies(And(0 + cpu_deq_cnt_at_time_2 < 4, True),
        Not(cha_index_3_time_3_val))
cons_fifo_condition3_for_cha_index_4_at_time_3 -> 
 Implies(And(0 + cpu_deq_cnt_at_time_2 < 5, True),
        Not(cha_index_4_time_3_val))
cons_fifo_condition3_for_cha_index_5_at_time_3 -> 
 Implies(And(0 + cpu_deq_cnt_at_time_2 < 6, True),
        Not(cha_index_5_time_3_val))
cons_init_llc_replace_state -> 
 And(And(Not(llc_index_0_time_0_valid),
        llc_index_0_time_0_lastAcc == 0,
        llc_index_0_time_0_hits == 0),
    And(Not(llc_index_1_time_0_valid),
        llc_index_1_time_0_lastAcc == 0,
        llc_index_1_time_0_hits == 0),
    And(Not(llc_index_2_time_0_valid),
        llc_index_2_time_0_lastAcc == 0,
        llc_index_2_time_0_hits == 0),
    And(Not(llc_index_3_time_0_valid),
        llc_index_3_time_0_lastAcc == 0,
        llc_index_3_time_0_hits == 0))
cons_llc_replace_index_0_at_time_0 -> 
 If(llc_replace_index_0_at_time_0,
   Or(If(mc_deq_cnt_at_time_0 > 0,
         And(llc_index_0_time_1_loc == mc_index_0_time_0_loc,
             llc_index_0_time_1_lastAcc == 1,
             llc_index_0_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 1,
         And(llc_index_0_time_1_loc == mc_index_1_time_0_loc,
             llc_index_0_time_1_lastAcc == 1,
             llc_index_0_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 2,
         And(llc_index_0_time_1_loc == mc_index_2_time_0_loc,
             llc_index_0_time_1_lastAcc == 1,
             llc_index_0_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 3,
         And(llc_index_0_time_1_loc == mc_index_3_time_0_loc,
             llc_index_0_time_1_lastAcc == 1,
             llc_index_0_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 4,
         And(llc_index_0_time_1_loc == mc_index_4_time_0_loc,
             llc_index_0_time_1_lastAcc == 1,
             llc_index_0_time_1_valid),
         False)),
   And(llc_index_0_time_1_valid == llc_index_0_time_0_valid,
       llc_index_0_time_1_lastAcc ==
       llc_index_0_time_0_lastAcc,
       llc_index_0_time_1_loc == llc_index_0_time_0_loc))
cons_llc_replace_index_1_at_time_0 -> 
 If(llc_replace_index_1_at_time_0,
   Or(If(mc_deq_cnt_at_time_0 > 0,
         And(llc_index_1_time_1_loc == mc_index_0_time_0_loc,
             llc_index_1_time_1_lastAcc == 1,
             llc_index_1_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 1,
         And(llc_index_1_time_1_loc == mc_index_1_time_0_loc,
             llc_index_1_time_1_lastAcc == 1,
             llc_index_1_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 2,
         And(llc_index_1_time_1_loc == mc_index_2_time_0_loc,
             llc_index_1_time_1_lastAcc == 1,
             llc_index_1_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 3,
         And(llc_index_1_time_1_loc == mc_index_3_time_0_loc,
             llc_index_1_time_1_lastAcc == 1,
             llc_index_1_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 4,
         And(llc_index_1_time_1_loc == mc_index_4_time_0_loc,
             llc_index_1_time_1_lastAcc == 1,
             llc_index_1_time_1_valid),
         False)),
   And(llc_index_1_time_1_valid == llc_index_1_time_0_valid,
       llc_index_1_time_1_lastAcc ==
       llc_index_1_time_0_lastAcc,
       llc_index_1_time_1_loc == llc_index_1_time_0_loc))
cons_llc_replace_index_2_at_time_0 -> 
 If(llc_replace_index_2_at_time_0,
   Or(If(mc_deq_cnt_at_time_0 > 0,
         And(llc_index_2_time_1_loc == mc_index_0_time_0_loc,
             llc_index_2_time_1_lastAcc == 1,
             llc_index_2_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 1,
         And(llc_index_2_time_1_loc == mc_index_1_time_0_loc,
             llc_index_2_time_1_lastAcc == 1,
             llc_index_2_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 2,
         And(llc_index_2_time_1_loc == mc_index_2_time_0_loc,
             llc_index_2_time_1_lastAcc == 1,
             llc_index_2_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 3,
         And(llc_index_2_time_1_loc == mc_index_3_time_0_loc,
             llc_index_2_time_1_lastAcc == 1,
             llc_index_2_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 4,
         And(llc_index_2_time_1_loc == mc_index_4_time_0_loc,
             llc_index_2_time_1_lastAcc == 1,
             llc_index_2_time_1_valid),
         False)),
   And(llc_index_2_time_1_valid == llc_index_2_time_0_valid,
       llc_index_2_time_1_lastAcc ==
       llc_index_2_time_0_lastAcc,
       llc_index_2_time_1_loc == llc_index_2_time_0_loc))
cons_llc_replace_index_3_at_time_0 -> 
 If(llc_replace_index_3_at_time_0,
   Or(If(mc_deq_cnt_at_time_0 > 0,
         And(llc_index_3_time_1_loc == mc_index_0_time_0_loc,
             llc_index_3_time_1_lastAcc == 1,
             llc_index_3_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 1,
         And(llc_index_3_time_1_loc == mc_index_1_time_0_loc,
             llc_index_3_time_1_lastAcc == 1,
             llc_index_3_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 2,
         And(llc_index_3_time_1_loc == mc_index_2_time_0_loc,
             llc_index_3_time_1_lastAcc == 1,
             llc_index_3_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 3,
         And(llc_index_3_time_1_loc == mc_index_3_time_0_loc,
             llc_index_3_time_1_lastAcc == 1,
             llc_index_3_time_1_valid),
         False),
      If(mc_deq_cnt_at_time_0 > 4,
         And(llc_index_3_time_1_loc == mc_index_4_time_0_loc,
             llc_index_3_time_1_lastAcc == 1,
             llc_index_3_time_1_valid),
         False)),
   And(llc_index_3_time_1_valid == llc_index_3_time_0_valid,
       llc_index_3_time_1_lastAcc ==
       llc_index_3_time_0_lastAcc,
       llc_index_3_time_1_loc == llc_index_3_time_0_loc))
cons_llc_replace_index_0_at_time_1 -> 
 If(llc_replace_index_0_at_time_1,
   Or(If(mc_deq_cnt_at_time_1 > 0,
         And(llc_index_0_time_2_loc == mc_index_0_time_1_loc,
             llc_index_0_time_2_lastAcc == 2,
             llc_index_0_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 1,
         And(llc_index_0_time_2_loc == mc_index_1_time_1_loc,
             llc_index_0_time_2_lastAcc == 2,
             llc_index_0_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 2,
         And(llc_index_0_time_2_loc == mc_index_2_time_1_loc,
             llc_index_0_time_2_lastAcc == 2,
             llc_index_0_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 3,
         And(llc_index_0_time_2_loc == mc_index_3_time_1_loc,
             llc_index_0_time_2_lastAcc == 2,
             llc_index_0_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 4,
         And(llc_index_0_time_2_loc == mc_index_4_time_1_loc,
             llc_index_0_time_2_lastAcc == 2,
             llc_index_0_time_2_valid),
         False)),
   And(llc_index_0_time_2_valid == llc_index_0_time_1_valid,
       llc_index_0_time_2_lastAcc ==
       llc_index_0_time_1_lastAcc,
       llc_index_0_time_2_loc == llc_index_0_time_1_loc))
cons_llc_replace_index_1_at_time_1 -> 
 If(llc_replace_index_1_at_time_1,
   Or(If(mc_deq_cnt_at_time_1 > 0,
         And(llc_index_1_time_2_loc == mc_index_0_time_1_loc,
             llc_index_1_time_2_lastAcc == 2,
             llc_index_1_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 1,
         And(llc_index_1_time_2_loc == mc_index_1_time_1_loc,
             llc_index_1_time_2_lastAcc == 2,
             llc_index_1_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 2,
         And(llc_index_1_time_2_loc == mc_index_2_time_1_loc,
             llc_index_1_time_2_lastAcc == 2,
             llc_index_1_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 3,
         And(llc_index_1_time_2_loc == mc_index_3_time_1_loc,
             llc_index_1_time_2_lastAcc == 2,
             llc_index_1_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 4,
         And(llc_index_1_time_2_loc == mc_index_4_time_1_loc,
             llc_index_1_time_2_lastAcc == 2,
             llc_index_1_time_2_valid),
         False)),
   And(llc_index_1_time_2_valid == llc_index_1_time_1_valid,
       llc_index_1_time_2_lastAcc ==
       llc_index_1_time_1_lastAcc,
       llc_index_1_time_2_loc == llc_index_1_time_1_loc))
cons_llc_replace_index_2_at_time_1 -> 
 If(llc_replace_index_2_at_time_1,
   Or(If(mc_deq_cnt_at_time_1 > 0,
         And(llc_index_2_time_2_loc == mc_index_0_time_1_loc,
             llc_index_2_time_2_lastAcc == 2,
             llc_index_2_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 1,
         And(llc_index_2_time_2_loc == mc_index_1_time_1_loc,
             llc_index_2_time_2_lastAcc == 2,
             llc_index_2_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 2,
         And(llc_index_2_time_2_loc == mc_index_2_time_1_loc,
             llc_index_2_time_2_lastAcc == 2,
             llc_index_2_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 3,
         And(llc_index_2_time_2_loc == mc_index_3_time_1_loc,
             llc_index_2_time_2_lastAcc == 2,
             llc_index_2_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 4,
         And(llc_index_2_time_2_loc == mc_index_4_time_1_loc,
             llc_index_2_time_2_lastAcc == 2,
             llc_index_2_time_2_valid),
         False)),
   And(llc_index_2_time_2_valid == llc_index_2_time_1_valid,
       llc_index_2_time_2_lastAcc ==
       llc_index_2_time_1_lastAcc,
       llc_index_2_time_2_loc == llc_index_2_time_1_loc))
cons_llc_replace_index_3_at_time_1 -> 
 If(llc_replace_index_3_at_time_1,
   Or(If(mc_deq_cnt_at_time_1 > 0,
         And(llc_index_3_time_2_loc == mc_index_0_time_1_loc,
             llc_index_3_time_2_lastAcc == 2,
             llc_index_3_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 1,
         And(llc_index_3_time_2_loc == mc_index_1_time_1_loc,
             llc_index_3_time_2_lastAcc == 2,
             llc_index_3_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 2,
         And(llc_index_3_time_2_loc == mc_index_2_time_1_loc,
             llc_index_3_time_2_lastAcc == 2,
             llc_index_3_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 3,
         And(llc_index_3_time_2_loc == mc_index_3_time_1_loc,
             llc_index_3_time_2_lastAcc == 2,
             llc_index_3_time_2_valid),
         False),
      If(mc_deq_cnt_at_time_1 > 4,
         And(llc_index_3_time_2_loc == mc_index_4_time_1_loc,
             llc_index_3_time_2_lastAcc == 2,
             llc_index_3_time_2_valid),
         False)),
   And(llc_index_3_time_2_valid == llc_index_3_time_1_valid,
       llc_index_3_time_2_lastAcc ==
       llc_index_3_time_1_lastAcc,
       llc_index_3_time_2_loc == llc_index_3_time_1_loc))
cons_llc_replace_index_0_at_time_3 -> 
 If(llc_replace_index_0_at_time_3,
   Or(If(mc_deq_cnt_at_time_3 > 0,
         And(llc_index_0_time_4_loc == mc_index_0_time_3_loc,
             llc_index_0_time_4_lastAcc == 4,
             llc_index_0_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 1,
         And(llc_index_0_time_4_loc == mc_index_1_time_3_loc,
             llc_index_0_time_4_lastAcc == 4,
             llc_index_0_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 2,
         And(llc_index_0_time_4_loc == mc_index_2_time_3_loc,
             llc_index_0_time_4_lastAcc == 4,
             llc_index_0_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 3,
         And(llc_index_0_time_4_loc == mc_index_3_time_3_loc,
             llc_index_0_time_4_lastAcc == 4,
             llc_index_0_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 4,
         And(llc_index_0_time_4_loc == mc_index_4_time_3_loc,
             llc_index_0_time_4_lastAcc == 4,
             llc_index_0_time_4_valid),
         False)),
   And(llc_index_0_time_4_valid == llc_index_0_time_3_valid,
       llc_index_0_time_4_lastAcc ==
       llc_index_0_time_3_lastAcc,
       llc_index_0_time_4_loc == llc_index_0_time_3_loc))
cons_llc_replace_index_1_at_time_3 -> 
 If(llc_replace_index_1_at_time_3,
   Or(If(mc_deq_cnt_at_time_3 > 0,
         And(llc_index_1_time_4_loc == mc_index_0_time_3_loc,
             llc_index_1_time_4_lastAcc == 4,
             llc_index_1_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 1,
         And(llc_index_1_time_4_loc == mc_index_1_time_3_loc,
             llc_index_1_time_4_lastAcc == 4,
             llc_index_1_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 2,
         And(llc_index_1_time_4_loc == mc_index_2_time_3_loc,
             llc_index_1_time_4_lastAcc == 4,
             llc_index_1_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 3,
         And(llc_index_1_time_4_loc == mc_index_3_time_3_loc,
             llc_index_1_time_4_lastAcc == 4,
             llc_index_1_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 4,
         And(llc_index_1_time_4_loc == mc_index_4_time_3_loc,
             llc_index_1_time_4_lastAcc == 4,
             llc_index_1_time_4_valid),
         False)),
   And(llc_index_1_time_4_valid == llc_index_1_time_3_valid,
       llc_index_1_time_4_lastAcc ==
       llc_index_1_time_3_lastAcc,
       llc_index_1_time_4_loc == llc_index_1_time_3_loc))
cons_llc_replace_index_2_at_time_3 -> 
 If(llc_replace_index_2_at_time_3,
   Or(If(mc_deq_cnt_at_time_3 > 0,
         And(llc_index_2_time_4_loc == mc_index_0_time_3_loc,
             llc_index_2_time_4_lastAcc == 4,
             llc_index_2_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 1,
         And(llc_index_2_time_4_loc == mc_index_1_time_3_loc,
             llc_index_2_time_4_lastAcc == 4,
             llc_index_2_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 2,
         And(llc_index_2_time_4_loc == mc_index_2_time_3_loc,
             llc_index_2_time_4_lastAcc == 4,
             llc_index_2_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 3,
         And(llc_index_2_time_4_loc == mc_index_3_time_3_loc,
             llc_index_2_time_4_lastAcc == 4,
             llc_index_2_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 4,
         And(llc_index_2_time_4_loc == mc_index_4_time_3_loc,
             llc_index_2_time_4_lastAcc == 4,
             llc_index_2_time_4_valid),
         False)),
   And(llc_index_2_time_4_valid == llc_index_2_time_3_valid,
       llc_index_2_time_4_lastAcc ==
       llc_index_2_time_3_lastAcc,
       llc_index_2_time_4_loc == llc_index_2_time_3_loc))
cons_llc_replace_index_3_at_time_3 -> 
 If(llc_replace_index_3_at_time_3,
   Or(If(mc_deq_cnt_at_time_3 > 0,
         And(llc_index_3_time_4_loc == mc_index_0_time_3_loc,
             llc_index_3_time_4_lastAcc == 4,
             llc_index_3_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 1,
         And(llc_index_3_time_4_loc == mc_index_1_time_3_loc,
             llc_index_3_time_4_lastAcc == 4,
             llc_index_3_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 2,
         And(llc_index_3_time_4_loc == mc_index_2_time_3_loc,
             llc_index_3_time_4_lastAcc == 4,
             llc_index_3_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 3,
         And(llc_index_3_time_4_loc == mc_index_3_time_3_loc,
             llc_index_3_time_4_lastAcc == 4,
             llc_index_3_time_4_valid),
         False),
      If(mc_deq_cnt_at_time_3 > 4,
         And(llc_index_3_time_4_loc == mc_index_4_time_3_loc,
             llc_index_3_time_4_lastAcc == 4,
             llc_index_3_time_4_valid),
         False)),
   And(llc_index_3_time_4_valid == llc_index_3_time_3_valid,
       llc_index_3_time_4_lastAcc ==
       llc_index_3_time_3_lastAcc,
       llc_index_3_time_4_loc == llc_index_3_time_3_loc))
cons_llc_distinct_*73 -> 
 Implies(And(llc_replace_index_0_at_time_3,
            llc_replace_index_1_at_time_3),
        llc_index_0_time_4_loc != llc_index_1_time_4_loc)
cons_llc_distinct_*75 -> 
 Implies(And(llc_replace_index_0_at_time_3,
            llc_replace_index_2_at_time_3),
        llc_index_0_time_4_loc != llc_index_2_time_4_loc)
cons_llc_distinct_*77 -> 
 Implies(And(llc_replace_index_0_at_time_3,
            llc_replace_index_3_at_time_3),
        llc_index_0_time_4_loc != llc_index_3_time_4_loc)
cons_llc_distinct_*81 -> 
 Implies(And(llc_replace_index_1_at_time_3,
            llc_replace_index_2_at_time_3),
        llc_index_1_time_4_loc != llc_index_2_time_4_loc)
cons_llc_distinct_*83 -> 
 Implies(And(llc_replace_index_1_at_time_3,
            llc_replace_index_3_at_time_3),
        llc_index_1_time_4_loc != llc_index_3_time_4_loc)
cons_llc_distinct_*89 -> 
 Implies(And(llc_replace_index_2_at_time_3,
            llc_replace_index_3_at_time_3),
        llc_index_2_time_4_loc != llc_index_3_time_4_loc)
cons_llc_replace_index_0_at_time_4 -> 
 If(llc_replace_index_0_at_time_4,
   Or(If(mc_deq_cnt_at_time_4 > 0,
         And(llc_index_0_time_5_loc == mc_index_0_time_4_loc,
             llc_index_0_time_5_lastAcc == 5,
             llc_index_0_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 1,
         And(llc_index_0_time_5_loc == mc_index_1_time_4_loc,
             llc_index_0_time_5_lastAcc == 5,
             llc_index_0_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 2,
         And(llc_index_0_time_5_loc == mc_index_2_time_4_loc,
             llc_index_0_time_5_lastAcc == 5,
             llc_index_0_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 3,
         And(llc_index_0_time_5_loc == mc_index_3_time_4_loc,
             llc_index_0_time_5_lastAcc == 5,
             llc_index_0_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 4,
         And(llc_index_0_time_5_loc == mc_index_4_time_4_loc,
             llc_index_0_time_5_lastAcc == 5,
             llc_index_0_time_5_valid),
         False)),
   And(llc_index_0_time_5_valid == llc_index_0_time_4_valid,
       llc_index_0_time_5_lastAcc ==
       llc_index_0_time_4_lastAcc,
       llc_index_0_time_5_loc == llc_index_0_time_4_loc))
cons_llc_replace_index_1_at_time_4 -> 
 If(llc_replace_index_1_at_time_4,
   Or(If(mc_deq_cnt_at_time_4 > 0,
         And(llc_index_1_time_5_loc == mc_index_0_time_4_loc,
             llc_index_1_time_5_lastAcc == 5,
             llc_index_1_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 1,
         And(llc_index_1_time_5_loc == mc_index_1_time_4_loc,
             llc_index_1_time_5_lastAcc == 5,
             llc_index_1_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 2,
         And(llc_index_1_time_5_loc == mc_index_2_time_4_loc,
             llc_index_1_time_5_lastAcc == 5,
             llc_index_1_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 3,
         And(llc_index_1_time_5_loc == mc_index_3_time_4_loc,
             llc_index_1_time_5_lastAcc == 5,
             llc_index_1_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 4,
         And(llc_index_1_time_5_loc == mc_index_4_time_4_loc,
             llc_index_1_time_5_lastAcc == 5,
             llc_index_1_time_5_valid),
         False)),
   And(llc_index_1_time_5_valid == llc_index_1_time_4_valid,
       llc_index_1_time_5_lastAcc ==
       llc_index_1_time_4_lastAcc,
       llc_index_1_time_5_loc == llc_index_1_time_4_loc))
cons_llc_replace_index_2_at_time_4 -> 
 If(llc_replace_index_2_at_time_4,
   Or(If(mc_deq_cnt_at_time_4 > 0,
         And(llc_index_2_time_5_loc == mc_index_0_time_4_loc,
             llc_index_2_time_5_lastAcc == 5,
             llc_index_2_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 1,
         And(llc_index_2_time_5_loc == mc_index_1_time_4_loc,
             llc_index_2_time_5_lastAcc == 5,
             llc_index_2_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 2,
         And(llc_index_2_time_5_loc == mc_index_2_time_4_loc,
             llc_index_2_time_5_lastAcc == 5,
             llc_index_2_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 3,
         And(llc_index_2_time_5_loc == mc_index_3_time_4_loc,
             llc_index_2_time_5_lastAcc == 5,
             llc_index_2_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 4,
         And(llc_index_2_time_5_loc == mc_index_4_time_4_loc,
             llc_index_2_time_5_lastAcc == 5,
             llc_index_2_time_5_valid),
         False)),
   And(llc_index_2_time_5_valid == llc_index_2_time_4_valid,
       llc_index_2_time_5_lastAcc ==
       llc_index_2_time_4_lastAcc,
       llc_index_2_time_5_loc == llc_index_2_time_4_loc))
cons_llc_replace_index_3_at_time_4 -> 
 If(llc_replace_index_3_at_time_4,
   Or(If(mc_deq_cnt_at_time_4 > 0,
         And(llc_index_3_time_5_loc == mc_index_0_time_4_loc,
             llc_index_3_time_5_lastAcc == 5,
             llc_index_3_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 1,
         And(llc_index_3_time_5_loc == mc_index_1_time_4_loc,
             llc_index_3_time_5_lastAcc == 5,
             llc_index_3_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 2,
         And(llc_index_3_time_5_loc == mc_index_2_time_4_loc,
             llc_index_3_time_5_lastAcc == 5,
             llc_index_3_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 3,
         And(llc_index_3_time_5_loc == mc_index_3_time_4_loc,
             llc_index_3_time_5_lastAcc == 5,
             llc_index_3_time_5_valid),
         False),
      If(mc_deq_cnt_at_time_4 > 4,
         And(llc_index_3_time_5_loc == mc_index_4_time_4_loc,
             llc_index_3_time_5_lastAcc == 5,
             llc_index_3_time_5_valid),
         False)),
   And(llc_index_3_time_5_valid == llc_index_3_time_4_valid,
       llc_index_3_time_5_lastAcc ==
       llc_index_3_time_4_lastAcc,
       llc_index_3_time_5_loc == llc_index_3_time_4_loc))
cons_cha_hit_index_0_at_time_1 -> 
 cha_hit_index_0_at_time_1 ==
If(cha_index_0_time_1_val,
   If(Or(And(llc_index_0_time_1_loc ==
             cha_index_0_time_1_loc,
             llc_index_0_time_1_valid),
         And(llc_index_1_time_1_loc ==
             cha_index_0_time_1_loc,
             llc_index_1_time_1_valid),
         And(llc_index_2_time_1_loc ==
             cha_index_0_time_1_loc,
             llc_index_2_time_1_valid),
         And(llc_index_3_time_1_loc ==
             cha_index_0_time_1_loc,
             llc_index_3_time_1_valid)),
      True,
      False),
   False)
cons_cha_hit_index_1_at_time_1 -> 
 cha_hit_index_1_at_time_1 ==
If(cha_index_1_time_1_val,
   If(Or(And(llc_index_0_time_1_loc ==
             cha_index_1_time_1_loc,
             llc_index_0_time_1_valid),
         And(llc_index_1_time_1_loc ==
             cha_index_1_time_1_loc,
             llc_index_1_time_1_valid),
         And(llc_index_2_time_1_loc ==
             cha_index_1_time_1_loc,
             llc_index_2_time_1_valid),
         And(llc_index_3_time_1_loc ==
             cha_index_1_time_1_loc,
             llc_index_3_time_1_valid)),
      True,
      False),
   False)
cons_cha_hit_index_2_at_time_1 -> 
 cha_hit_index_2_at_time_1 ==
If(cha_index_2_time_1_val,
   If(Or(And(llc_index_0_time_1_loc ==
             cha_index_2_time_1_loc,
             llc_index_0_time_1_valid),
         And(llc_index_1_time_1_loc ==
             cha_index_2_time_1_loc,
             llc_index_1_time_1_valid),
         And(llc_index_2_time_1_loc ==
             cha_index_2_time_1_loc,
             llc_index_2_time_1_valid),
         And(llc_index_3_time_1_loc ==
             cha_index_2_time_1_loc,
             llc_index_3_time_1_valid)),
      True,
      False),
   False)
cons_cha_hit_index_3_at_time_1 -> 
 cha_hit_index_3_at_time_1 ==
If(cha_index_3_time_1_val,
   If(Or(And(llc_index_0_time_1_loc ==
             cha_index_3_time_1_loc,
             llc_index_0_time_1_valid),
         And(llc_index_1_time_1_loc ==
             cha_index_3_time_1_loc,
             llc_index_1_time_1_valid),
         And(llc_index_2_time_1_loc ==
             cha_index_3_time_1_loc,
             llc_index_2_time_1_valid),
         And(llc_index_3_time_1_loc ==
             cha_index_3_time_1_loc,
             llc_index_3_time_1_valid)),
      True,
      False),
   False)
cons_cha_hit_index_4_at_time_1 -> 
 cha_hit_index_4_at_time_1 ==
If(cha_index_4_time_1_val,
   If(Or(And(llc_index_0_time_1_loc ==
             cha_index_4_time_1_loc,
             llc_index_0_time_1_valid),
         And(llc_index_1_time_1_loc ==
             cha_index_4_time_1_loc,
             llc_index_1_time_1_valid),
         And(llc_index_2_time_1_loc ==
             cha_index_4_time_1_loc,
             llc_index_2_time_1_valid),
         And(llc_index_3_time_1_loc ==
             cha_index_4_time_1_loc,
             llc_index_3_time_1_valid)),
      True,
      False),
   False)
cons_cha_hit_index_5_at_time_1 -> 
 cha_hit_index_5_at_time_1 ==
If(cha_index_5_time_1_val,
   If(Or(And(llc_index_0_time_1_loc ==
             cha_index_5_time_1_loc,
             llc_index_0_time_1_valid),
         And(llc_index_1_time_1_loc ==
             cha_index_5_time_1_loc,
             llc_index_1_time_1_valid),
         And(llc_index_2_time_1_loc ==
             cha_index_5_time_1_loc,
             llc_index_2_time_1_valid),
         And(llc_index_3_time_1_loc ==
             cha_index_5_time_1_loc,
             llc_index_3_time_1_valid)),
      True,
      False),
   False)
cons_cha_sd_non_hit_index_0_raw_0_at_time_1 -> 
 Implies(And(And(6 - cha_sd_cap_cnt_at_time_1 <= 0,
                6 - cha_sd_cap_cnt_at_time_1 +
                cha_val_cnt_at_time_1 -
                (If(cha_hit_index_0_at_time_1, 1, 0) +
                 If(cha_hit_index_1_at_time_1, 1, 0) +
                 If(cha_hit_index_2_at_time_1, 1, 0) +
                 If(cha_hit_index_3_at_time_1, 1, 0) +
                 If(cha_hit_index_4_at_time_1, 1, 0) +
                 If(cha_hit_index_5_at_time_1, 1, 0)) >
                0,
                0 - (6 - cha_sd_cap_cnt_at_time_1) == 0),
            If(cha_hit_index_0_at_time_1, 1, 0) ==
            0 - (0 - (6 - cha_sd_cap_cnt_at_time_1))),
        And(cha_index_0_time_1_val ==
            cha_sd_index_0_time_1_val,
            cha_index_0_time_1_src ==
            cha_sd_index_0_time_1_src,
            cha_index_0_time_1_loc ==
            cha_sd_index_0_time_1_loc,
            cha_index_0_time_1_stime ==
            cha_sd_index_0_time_1_stime))
cons_cha_sd_non_hit_index_1_raw_1_at_time_1_*225 -> 
 Implies(And(And(6 - cha_sd_cap_cnt_at_time_1 <= 1,
                6 - cha_sd_cap_cnt_at_time_1 +
                cha_val_cnt_at_time_1 -
                (If(cha_hit_index_0_at_time_1, 1, 0) +
                 If(cha_hit_index_1_at_time_1, 1, 0) +
                 If(cha_hit_index_2_at_time_1, 1, 0) +
                 If(cha_hit_index_3_at_time_1, 1, 0) +
                 If(cha_hit_index_4_at_time_1, 1, 0) +
                 If(cha_hit_index_5_at_time_1, 1, 0)) >
                1,
                1 - (6 - cha_sd_cap_cnt_at_time_1) == 1),
            If(cha_hit_index_0_at_time_1, 1, 0) +
            If(cha_hit_index_1_at_time_1, 1, 0) ==
            1 - (1 - (6 - cha_sd_cap_cnt_at_time_1))),
        And(cha_index_1_time_1_val ==
            cha_sd_index_1_time_1_val,
            cha_index_1_time_1_src ==
            cha_sd_index_1_time_1_src,
            cha_index_1_time_1_loc ==
            cha_sd_index_1_time_1_loc,
            cha_index_1_time_1_stime ==
            cha_sd_index_1_time_1_stime))
cons_cha_sd_non_hit_index_2_raw_2_at_time_1_*245 -> 
 Implies(And(And(6 - cha_sd_cap_cnt_at_time_1 <= 2,
                6 - cha_sd_cap_cnt_at_time_1 +
                cha_val_cnt_at_time_1 -
                (If(cha_hit_index_0_at_time_1, 1, 0) +
                 If(cha_hit_index_1_at_time_1, 1, 0) +
                 If(cha_hit_index_2_at_time_1, 1, 0) +
                 If(cha_hit_index_3_at_time_1, 1, 0) +
                 If(cha_hit_index_4_at_time_1, 1, 0) +
                 If(cha_hit_index_5_at_time_1, 1, 0)) >
                2,
                2 - (6 - cha_sd_cap_cnt_at_time_1) == 2),
            If(cha_hit_index_0_at_time_1, 1, 0) +
            If(cha_hit_index_1_at_time_1, 1, 0) +
            If(cha_hit_index_2_at_time_1, 1, 0) ==
            2 - (2 - (6 - cha_sd_cap_cnt_at_time_1))),
        And(cha_index_2_time_1_val ==
            cha_sd_index_2_time_1_val,
            cha_index_2_time_1_src ==
            cha_sd_index_2_time_1_src,
            cha_index_2_time_1_loc ==
            cha_sd_index_2_time_1_loc,
            cha_index_2_time_1_stime ==
            cha_sd_index_2_time_1_stime))
cons_cha_sd_non_hit_index_3_raw_3_at_time_1_*264 -> 
 Implies(And(And(6 - cha_sd_cap_cnt_at_time_1 <= 3,
                6 - cha_sd_cap_cnt_at_time_1 +
                cha_val_cnt_at_time_1 -
                (If(cha_hit_index_0_at_time_1, 1, 0) +
                 If(cha_hit_index_1_at_time_1, 1, 0) +
                 If(cha_hit_index_2_at_time_1, 1, 0) +
                 If(cha_hit_index_3_at_time_1, 1, 0) +
                 If(cha_hit_index_4_at_time_1, 1, 0) +
                 If(cha_hit_index_5_at_time_1, 1, 0)) >
                3,
                3 - (6 - cha_sd_cap_cnt_at_time_1) == 3),
            If(cha_hit_index_0_at_time_1, 1, 0) +
            If(cha_hit_index_1_at_time_1, 1, 0) +
            If(cha_hit_index_2_at_time_1, 1, 0) +
            If(cha_hit_index_3_at_time_1, 1, 0) ==
            3 - (3 - (6 - cha_sd_cap_cnt_at_time_1))),
        And(cha_index_3_time_1_val ==
            cha_sd_index_3_time_1_val,
            cha_index_3_time_1_src ==
            cha_sd_index_3_time_1_src,
            cha_index_3_time_1_loc ==
            cha_sd_index_3_time_1_loc,
            cha_index_3_time_1_stime ==
            cha_sd_index_3_time_1_stime))
cons_cha_sd_non_hit_index_4_raw_4_at_time_1_*282 -> 
 Implies(And(And(6 - cha_sd_cap_cnt_at_time_1 <= 4,
                6 - cha_sd_cap_cnt_at_time_1 +
                cha_val_cnt_at_time_1 -
                (If(cha_hit_index_0_at_time_1, 1, 0) +
                 If(cha_hit_index_1_at_time_1, 1, 0) +
                 If(cha_hit_index_2_at_time_1, 1, 0) +
                 If(cha_hit_index_3_at_time_1, 1, 0) +
                 If(cha_hit_index_4_at_time_1, 1, 0) +
                 If(cha_hit_index_5_at_time_1, 1, 0)) >
                4,
                4 - (6 - cha_sd_cap_cnt_at_time_1) == 4),
            If(cha_hit_index_0_at_time_1, 1, 0) +
            If(cha_hit_index_1_at_time_1, 1, 0) +
            If(cha_hit_index_2_at_time_1, 1, 0) +
            If(cha_hit_index_3_at_time_1, 1, 0) +
            If(cha_hit_index_4_at_time_1, 1, 0) ==
            4 - (4 - (6 - cha_sd_cap_cnt_at_time_1))),
        And(cha_index_4_time_1_val ==
            cha_sd_index_4_time_1_val,
            cha_index_4_time_1_src ==
            cha_sd_index_4_time_1_src,
            cha_index_4_time_1_loc ==
            cha_sd_index_4_time_1_loc,
            cha_index_4_time_1_stime ==
            cha_sd_index_4_time_1_stime))
cons_cha_sd_non_hit_index_5_raw_5_at_time_1_*299 -> 
 Implies(And(And(6 - cha_sd_cap_cnt_at_time_1 <= 5,
                6 - cha_sd_cap_cnt_at_time_1 +
                cha_val_cnt_at_time_1 -
                (If(cha_hit_index_0_at_time_1, 1, 0) +
                 If(cha_hit_index_1_at_time_1, 1, 0) +
                 If(cha_hit_index_2_at_time_1, 1, 0) +
                 If(cha_hit_index_3_at_time_1, 1, 0) +
                 If(cha_hit_index_4_at_time_1, 1, 0) +
                 If(cha_hit_index_5_at_time_1, 1, 0)) >
                5,
                5 - (6 - cha_sd_cap_cnt_at_time_1) == 5),
            If(cha_hit_index_0_at_time_1, 1, 0) +
            If(cha_hit_index_1_at_time_1, 1, 0) +
            If(cha_hit_index_2_at_time_1, 1, 0) +
            If(cha_hit_index_3_at_time_1, 1, 0) +
            If(cha_hit_index_4_at_time_1, 1, 0) +
            If(cha_hit_index_5_at_time_1, 1, 0) ==
            5 - (5 - (6 - cha_sd_cap_cnt_at_time_1))),
        And(cha_index_5_time_1_val ==
            cha_sd_index_5_time_1_val,
            cha_index_5_time_1_src ==
            cha_sd_index_5_time_1_src,
            cha_index_5_time_1_loc ==
            cha_sd_index_5_time_1_loc,
            cha_index_5_time_1_stime ==
            cha_sd_index_5_time_1_stime))
cons_cha_hit_index_0_at_time_2 -> 
 cha_hit_index_0_at_time_2 ==
If(cha_index_0_time_2_val,
   If(Or(And(llc_index_0_time_2_loc ==
             cha_index_0_time_2_loc,
             llc_index_0_time_2_valid),
         And(llc_index_1_time_2_loc ==
             cha_index_0_time_2_loc,
             llc_index_1_time_2_valid),
         And(llc_index_2_time_2_loc ==
             cha_index_0_time_2_loc,
             llc_index_2_time_2_valid),
         And(llc_index_3_time_2_loc ==
             cha_index_0_time_2_loc,
             llc_index_3_time_2_valid)),
      True,
      False),
   False)
cons_cha_hit_index_1_at_time_2 -> 
 cha_hit_index_1_at_time_2 ==
If(cha_index_1_time_2_val,
   If(Or(And(llc_index_0_time_2_loc ==
             cha_index_1_time_2_loc,
             llc_index_0_time_2_valid),
         And(llc_index_1_time_2_loc ==
             cha_index_1_time_2_loc,
             llc_index_1_time_2_valid),
         And(llc_index_2_time_2_loc ==
             cha_index_1_time_2_loc,
             llc_index_2_time_2_valid),
         And(llc_index_3_time_2_loc ==
             cha_index_1_time_2_loc,
             llc_index_3_time_2_valid)),
      True,
      False),
   False)
cons_cha_hit_index_2_at_time_2 -> 
 cha_hit_index_2_at_time_2 ==
If(cha_index_2_time_2_val,
   If(Or(And(llc_index_0_time_2_loc ==
             cha_index_2_time_2_loc,
             llc_index_0_time_2_valid),
         And(llc_index_1_time_2_loc ==
             cha_index_2_time_2_loc,
             llc_index_1_time_2_valid),
         And(llc_index_2_time_2_loc ==
             cha_index_2_time_2_loc,
             llc_index_2_time_2_valid),
         And(llc_index_3_time_2_loc ==
             cha_index_2_time_2_loc,
             llc_index_3_time_2_valid)),
      True,
      False),
   False)
cons_cha_hit_index_3_at_time_2 -> 
 cha_hit_index_3_at_time_2 ==
If(cha_index_3_time_2_val,
   If(Or(And(llc_index_0_time_2_loc ==
             cha_index_3_time_2_loc,
             llc_index_0_time_2_valid),
         And(llc_index_1_time_2_loc ==
             cha_index_3_time_2_loc,
             llc_index_1_time_2_valid),
         And(llc_index_2_time_2_loc ==
             cha_index_3_time_2_loc,
             llc_index_2_time_2_valid),
         And(llc_index_3_time_2_loc ==
             cha_index_3_time_2_loc,
             llc_index_3_time_2_valid)),
      True,
      False),
   False)
cons_cha_hit_index_4_at_time_2 -> 
 cha_hit_index_4_at_time_2 ==
If(cha_index_4_time_2_val,
   If(Or(And(llc_index_0_time_2_loc ==
             cha_index_4_time_2_loc,
             llc_index_0_time_2_valid),
         And(llc_index_1_time_2_loc ==
             cha_index_4_time_2_loc,
             llc_index_1_time_2_valid),
         And(llc_index_2_time_2_loc ==
             cha_index_4_time_2_loc,
             llc_index_2_time_2_valid),
         And(llc_index_3_time_2_loc ==
             cha_index_4_time_2_loc,
             llc_index_3_time_2_valid)),
      True,
      False),
   False)
cons_cha_hit_index_5_at_time_2 -> 
 cha_hit_index_5_at_time_2 ==
If(cha_index_5_time_2_val,
   If(Or(And(llc_index_0_time_2_loc ==
             cha_index_5_time_2_loc,
             llc_index_0_time_2_valid),
         And(llc_index_1_time_2_loc ==
             cha_index_5_time_2_loc,
             llc_index_1_time_2_valid),
         And(llc_index_2_time_2_loc ==
             cha_index_5_time_2_loc,
             llc_index_2_time_2_valid),
         And(llc_index_3_time_2_loc ==
             cha_index_5_time_2_loc,
             llc_index_3_time_2_valid)),
      True,
      False),
   False)
cons_for_cha_sd_deq_5_index_0_at_time_2 -> 
 Implies(And(6 - cha_sd_cap_cnt_at_time_2 > 0,
            cha_sd_deq_cnt_at_time_1 == 5),
        And(cha_sd_index_5_time_1_val ==
            cha_sd_index_0_time_2_val,
            cha_sd_index_5_time_1_src ==
            cha_sd_index_0_time_2_src,
            cha_sd_index_5_time_1_loc ==
            cha_sd_index_0_time_2_loc,
            cha_sd_index_5_time_1_stime ==
            cha_sd_index_0_time_2_stime))
cons_cha_sd_non_hit_index_1_raw_0_at_time_2 -> 
 Implies(And(And(6 - cha_sd_cap_cnt_at_time_2 <= 1,
                6 - cha_sd_cap_cnt_at_time_2 +
                cha_val_cnt_at_time_2 -
                (If(cha_hit_index_0_at_time_2, 1, 0) +
                 If(cha_hit_index_1_at_time_2, 1, 0) +
                 If(cha_hit_index_2_at_time_2, 1, 0) +
                 If(cha_hit_index_3_at_time_2, 1, 0) +
                 If(cha_hit_index_4_at_time_2, 1, 0) +
                 If(cha_hit_index_5_at_time_2, 1, 0)) >
                1,
                1 - (6 - cha_sd_cap_cnt_at_time_2) == 0),
            If(cha_hit_index_0_at_time_2, 1, 0) ==
            0 - (1 - (6 - cha_sd_cap_cnt_at_time_2))),
        And(cha_index_0_time_2_val ==
            cha_sd_index_1_time_2_val,
            cha_index_0_time_2_src ==
            cha_sd_index_1_time_2_src,
            cha_index_0_time_2_loc ==
            cha_sd_index_1_time_2_loc,
            cha_index_0_time_2_stime ==
            cha_sd_index_1_time_2_stime))
cons_cha_sd_invalid_index_2_at_time_2 -> 
 Implies(And(6 - cha_sd_cap_cnt_at_time_2 +
            cha_val_cnt_at_time_2 -
            (If(cha_hit_index_0_at_time_2, 1, 0) +
             If(cha_hit_index_1_at_time_2, 1, 0) +
             If(cha_hit_index_2_at_time_2, 1, 0) +
             If(cha_hit_index_3_at_time_2, 1, 0) +
             If(cha_hit_index_4_at_time_2, 1, 0) +
             If(cha_hit_index_5_at_time_2, 1, 0)) <=
            2),
        Not(cha_sd_index_2_time_2_val))
cons_cha_sd_invalid_index_3_at_time_2 -> 
 Implies(And(6 - cha_sd_cap_cnt_at_time_2 +
            cha_val_cnt_at_time_2 -
            (If(cha_hit_index_0_at_time_2, 1, 0) +
             If(cha_hit_index_1_at_time_2, 1, 0) +
             If(cha_hit_index_2_at_time_2, 1, 0) +
             If(cha_hit_index_3_at_time_2, 1, 0) +
             If(cha_hit_index_4_at_time_2, 1, 0) +
             If(cha_hit_index_5_at_time_2, 1, 0)) <=
            3),
        Not(cha_sd_index_3_time_2_val))
cons_cha_sd_invalid_index_4_at_time_2 -> 
 Implies(And(6 - cha_sd_cap_cnt_at_time_2 +
            cha_val_cnt_at_time_2 -
            (If(cha_hit_index_0_at_time_2, 1, 0) +
             If(cha_hit_index_1_at_time_2, 1, 0) +
             If(cha_hit_index_2_at_time_2, 1, 0) +
             If(cha_hit_index_3_at_time_2, 1, 0) +
             If(cha_hit_index_4_at_time_2, 1, 0) +
             If(cha_hit_index_5_at_time_2, 1, 0)) <=
            4),
        Not(cha_sd_index_4_time_2_val))
cons_cha_sd_invalid_index_5_at_time_2 -> 
 Implies(And(6 - cha_sd_cap_cnt_at_time_2 +
            cha_val_cnt_at_time_2 -
            (If(cha_hit_index_0_at_time_2, 1, 0) +
             If(cha_hit_index_1_at_time_2, 1, 0) +
             If(cha_hit_index_2_at_time_2, 1, 0) +
             If(cha_hit_index_3_at_time_2, 1, 0) +
             If(cha_hit_index_4_at_time_2, 1, 0) +
             If(cha_hit_index_5_at_time_2, 1, 0)) <=
            5),
        Not(cha_sd_index_5_time_2_val))
cons_cha_hit_index_0_at_time_3 -> 
 cha_hit_index_0_at_time_3 ==
If(cha_index_0_time_3_val,
   If(Or(And(llc_index_0_time_3_loc ==
             cha_index_0_time_3_loc,
             llc_index_0_time_3_valid),
         And(llc_index_1_time_3_loc ==
             cha_index_0_time_3_loc,
             llc_index_1_time_3_valid),
         And(llc_index_2_time_3_loc ==
             cha_index_0_time_3_loc,
             llc_index_2_time_3_valid),
         And(llc_index_3_time_3_loc ==
             cha_index_0_time_3_loc,
             llc_index_3_time_3_valid)),
      True,
      False),
   False)
cons_cha_hit_index_1_at_time_3 -> 
 cha_hit_index_1_at_time_3 ==
If(cha_index_1_time_3_val,
   If(Or(And(llc_index_0_time_3_loc ==
             cha_index_1_time_3_loc,
             llc_index_0_time_3_valid),
         And(llc_index_1_time_3_loc ==
             cha_index_1_time_3_loc,
             llc_index_1_time_3_valid),
         And(llc_index_2_time_3_loc ==
             cha_index_1_time_3_loc,
             llc_index_2_time_3_valid),
         And(llc_index_3_time_3_loc ==
             cha_index_1_time_3_loc,
             llc_index_3_time_3_valid)),
      True,
      False),
   False)
cons_cha_hit_index_2_at_time_3 -> 
 cha_hit_index_2_at_time_3 ==
If(cha_index_2_time_3_val,
   If(Or(And(llc_index_0_time_3_loc ==
             cha_index_2_time_3_loc,
             llc_index_0_time_3_valid),
         And(llc_index_1_time_3_loc ==
             cha_index_2_time_3_loc,
             llc_index_1_time_3_valid),
         And(llc_index_2_time_3_loc ==
             cha_index_2_time_3_loc,
             llc_index_2_time_3_valid),
         And(llc_index_3_time_3_loc ==
             cha_index_2_time_3_loc,
             llc_index_3_time_3_valid)),
      True,
      False),
   False)
cons_cha_hit_index_3_at_time_3 -> 
 cha_hit_index_3_at_time_3 ==
If(cha_index_3_time_3_val,
   If(Or(And(llc_index_0_time_3_loc ==
             cha_index_3_time_3_loc,
             llc_index_0_time_3_valid),
         And(llc_index_1_time_3_loc ==
             cha_index_3_time_3_loc,
             llc_index_1_time_3_valid),
         And(llc_index_2_time_3_loc ==
             cha_index_3_time_3_loc,
             llc_index_2_time_3_valid),
         And(llc_index_3_time_3_loc ==
             cha_index_3_time_3_loc,
             llc_index_3_time_3_valid)),
      True,
      False),
   False)
cons_cha_hit_index_4_at_time_3 -> 
 cha_hit_index_4_at_time_3 ==
If(cha_index_4_time_3_val,
   If(Or(And(llc_index_0_time_3_loc ==
             cha_index_4_time_3_loc,
             llc_index_0_time_3_valid),
         And(llc_index_1_time_3_loc ==
             cha_index_4_time_3_loc,
             llc_index_1_time_3_valid),
         And(llc_index_2_time_3_loc ==
             cha_index_4_time_3_loc,
             llc_index_2_time_3_valid),
         And(llc_index_3_time_3_loc ==
             cha_index_4_time_3_loc,
             llc_index_3_time_3_valid)),
      True,
      False),
   False)
cons_cha_hit_index_5_at_time_3 -> 
 cha_hit_index_5_at_time_3 ==
If(cha_index_5_time_3_val,
   If(Or(And(llc_index_0_time_3_loc ==
             cha_index_5_time_3_loc,
             llc_index_0_time_3_valid),
         And(llc_index_1_time_3_loc ==
             cha_index_5_time_3_loc,
             llc_index_1_time_3_valid),
         And(llc_index_2_time_3_loc ==
             cha_index_5_time_3_loc,
             llc_index_2_time_3_valid),
         And(llc_index_3_time_3_loc ==
             cha_index_5_time_3_loc,
             llc_index_3_time_3_valid)),
      True,
      False),
   False)
cons_cha_sd_invalid_index_0_at_time_3 -> 
 Implies(And(6 - cha_sd_cap_cnt_at_time_3 +
            cha_val_cnt_at_time_3 -
            (If(cha_hit_index_0_at_time_3, 1, 0) +
             If(cha_hit_index_1_at_time_3, 1, 0) +
             If(cha_hit_index_2_at_time_3, 1, 0) +
             If(cha_hit_index_3_at_time_3, 1, 0) +
             If(cha_hit_index_4_at_time_3, 1, 0) +
             If(cha_hit_index_5_at_time_3, 1, 0)) <=
            0),
        Not(cha_sd_index_0_time_3_val))
cons_cha_sd_invalid_index_1_at_time_3 -> 
 Implies(And(6 - cha_sd_cap_cnt_at_time_3 +
            cha_val_cnt_at_time_3 -
            (If(cha_hit_index_0_at_time_3, 1, 0) +
             If(cha_hit_index_1_at_time_3, 1, 0) +
             If(cha_hit_index_2_at_time_3, 1, 0) +
             If(cha_hit_index_3_at_time_3, 1, 0) +
             If(cha_hit_index_4_at_time_3, 1, 0) +
             If(cha_hit_index_5_at_time_3, 1, 0)) <=
            1),
        Not(cha_sd_index_1_time_3_val))
cons_cha_sd_invalid_index_2_at_time_3 -> 
 Implies(And(6 - cha_sd_cap_cnt_at_time_3 +
            cha_val_cnt_at_time_3 -
            (If(cha_hit_index_0_at_time_3, 1, 0) +
             If(cha_hit_index_1_at_time_3, 1, 0) +
             If(cha_hit_index_2_at_time_3, 1, 0) +
             If(cha_hit_index_3_at_time_3, 1, 0) +
             If(cha_hit_index_4_at_time_3, 1, 0) +
             If(cha_hit_index_5_at_time_3, 1, 0)) <=
            2),
        Not(cha_sd_index_2_time_3_val))
cons_cha_sd_invalid_index_3_at_time_3 -> 
 Implies(And(6 - cha_sd_cap_cnt_at_time_3 +
            cha_val_cnt_at_time_3 -
            (If(cha_hit_index_0_at_time_3, 1, 0) +
             If(cha_hit_index_1_at_time_3, 1, 0) +
             If(cha_hit_index_2_at_time_3, 1, 0) +
             If(cha_hit_index_3_at_time_3, 1, 0) +
             If(cha_hit_index_4_at_time_3, 1, 0) +
             If(cha_hit_index_5_at_time_3, 1, 0)) <=
            3),
        Not(cha_sd_index_3_time_3_val))
cons_cha_sd_invalid_index_4_at_time_3 -> 
 Implies(And(6 - cha_sd_cap_cnt_at_time_3 +
            cha_val_cnt_at_time_3 -
            (If(cha_hit_index_0_at_time_3, 1, 0) +
             If(cha_hit_index_1_at_time_3, 1, 0) +
             If(cha_hit_index_2_at_time_3, 1, 0) +
             If(cha_hit_index_3_at_time_3, 1, 0) +
             If(cha_hit_index_4_at_time_3, 1, 0) +
             If(cha_hit_index_5_at_time_3, 1, 0)) <=
            4),
        Not(cha_sd_index_4_time_3_val))
cons_cha_sd_invalid_index_5_at_time_3 -> 
 Implies(And(6 - cha_sd_cap_cnt_at_time_3 +
            cha_val_cnt_at_time_3 -
            (If(cha_hit_index_0_at_time_3, 1, 0) +
             If(cha_hit_index_1_at_time_3, 1, 0) +
             If(cha_hit_index_2_at_time_3, 1, 0) +
             If(cha_hit_index_3_at_time_3, 1, 0) +
             If(cha_hit_index_4_at_time_3, 1, 0) +
             If(cha_hit_index_5_at_time_3, 1, 0)) <=
            5),
        Not(cha_sd_index_5_time_3_val))
cons_cpu_credit_upt_at_time_0 -> 
 cpu_credit_cnt_at_time_1 ==
cpu_credit_cnt_at_time_0 - cpu_input_cnt_at_time_0 +
If(And(mc_deq_cnt_at_time_0 > 0,
       mc_index_0_time_0_src == cpu),
   1,
   0) +
If(And(mc_deq_cnt_at_time_0 > 1,
       mc_index_1_time_0_src == cpu),
   1,
   0) +
If(And(mc_deq_cnt_at_time_0 > 2,
       mc_index_2_time_0_src == cpu),
   1,
   0) +
If(And(mc_deq_cnt_at_time_0 > 3,
       mc_index_3_time_0_src == cpu),
   1,
   0) +
If(And(mc_deq_cnt_at_time_0 > 4,
       mc_index_4_time_0_src == cpu),
   1,
   0) +
If(And(cha_hit_index_0_at_time_0,
       cha_index_0_time_0_src == cpu),
   1,
   0) +
If(And(cha_hit_index_1_at_time_0,
       cha_index_1_time_0_src == cpu),
   1,
   0) +
If(And(cha_hit_index_2_at_time_0,
       cha_index_2_time_0_src == cpu),
   1,
   0) +
If(And(cha_hit_index_3_at_time_0,
       cha_index_3_time_0_src == cpu),
   1,
   0) +
If(And(cha_hit_index_4_at_time_0,
       cha_index_4_time_0_src == cpu),
   1,
   0) +
If(And(cha_hit_index_5_at_time_0,
       cha_index_5_time_0_src == cpu),
   1,
   0)
cons_cpu_credit_upt_at_time_1 -> 
 cpu_credit_cnt_at_time_2 ==
cpu_credit_cnt_at_time_1 - cpu_input_cnt_at_time_1 +
If(And(mc_deq_cnt_at_time_1 > 0,
       mc_index_0_time_1_src == cpu),
   1,
   0) +
If(And(mc_deq_cnt_at_time_1 > 1,
       mc_index_1_time_1_src == cpu),
   1,
   0) +
If(And(mc_deq_cnt_at_time_1 > 2,
       mc_index_2_time_1_src == cpu),
   1,
   0) +
If(And(mc_deq_cnt_at_time_1 > 3,
       mc_index_3_time_1_src == cpu),
   1,
   0) +
If(And(mc_deq_cnt_at_time_1 > 4,
       mc_index_4_time_1_src == cpu),
   1,
   0) +
If(And(cha_hit_index_0_at_time_1,
       cha_index_0_time_1_src == cpu),
   1,
   0) +
If(And(cha_hit_index_1_at_time_1,
       cha_index_1_time_1_src == cpu),
   1,
   0) +
If(And(cha_hit_index_2_at_time_1,
       cha_index_2_time_1_src == cpu),
   1,
   0) +
If(And(cha_hit_index_3_at_time_1,
       cha_index_3_time_1_src == cpu),
   1,
   0) +
If(And(cha_hit_index_4_at_time_1,
       cha_index_4_time_1_src == cpu),
   1,
   0) +
If(And(cha_hit_index_5_at_time_1,
       cha_index_5_time_1_src == cpu),
   1,
   0)
cons_for_cpu_flow_control_2_index_0_at_time_0 -> 
 Implies(And(7 - cpu_cap_cnt_at_time_0 <= 0,
            7 - cpu_cap_cnt_at_time_0 +
            cpu_input_cnt_at_time_0 >
            0),
        And(cpu_index_0_time_0_val,
            cpu_index_0_time_0_src == cpu,
            cpu_index_0_time_0_stime == 0))
cons_for_cpu_flow_control_2_index_1_at_time_0 -> 
 Implies(And(7 - cpu_cap_cnt_at_time_0 <= 1,
            7 - cpu_cap_cnt_at_time_0 +
            cpu_input_cnt_at_time_0 >
            1),
        And(cpu_index_1_time_0_val,
            cpu_index_1_time_0_src == cpu,
            cpu_index_1_time_0_stime == 1))
cons_for_cpu_flow_control_2_index_2_at_time_0 -> 
 Implies(And(7 - cpu_cap_cnt_at_time_0 <= 2,
            7 - cpu_cap_cnt_at_time_0 +
            cpu_input_cnt_at_time_0 >
            2),
        And(cpu_index_2_time_0_val,
            cpu_index_2_time_0_src == cpu,
            cpu_index_2_time_0_stime == 2))
cons_for_cpu_flow_control_2_index_3_at_time_0 -> 
 Implies(And(7 - cpu_cap_cnt_at_time_0 <= 3,
            7 - cpu_cap_cnt_at_time_0 +
            cpu_input_cnt_at_time_0 >
            3),
        And(cpu_index_3_time_0_val,
            cpu_index_3_time_0_src == cpu,
            cpu_index_3_time_0_stime == 3))
cons_for_cpu_flow_control_2_index_4_at_time_0 -> 
 Implies(And(7 - cpu_cap_cnt_at_time_0 <= 4,
            7 - cpu_cap_cnt_at_time_0 +
            cpu_input_cnt_at_time_0 >
            4),
        And(cpu_index_4_time_0_val,
            cpu_index_4_time_0_src == cpu,
            cpu_index_4_time_0_stime == 4))
cons_for_cpu_flow_control_2_index_5_at_time_0 -> 
 Implies(And(7 - cpu_cap_cnt_at_time_0 <= 5,
            7 - cpu_cap_cnt_at_time_0 +
            cpu_input_cnt_at_time_0 >
            5),
        And(cpu_index_5_time_0_val,
            cpu_index_5_time_0_src == cpu,
            cpu_index_5_time_0_stime == 5))
cons_for_cpu_flow_control_2_index_6_at_time_0 -> 
 Implies(And(7 - cpu_cap_cnt_at_time_0 <= 6,
            7 - cpu_cap_cnt_at_time_0 +
            cpu_input_cnt_at_time_0 >
            6),
        And(cpu_index_6_time_0_val,
            cpu_index_6_time_0_src == cpu,
            cpu_index_6_time_0_stime == 6))
cons_for_cpu_flow_control_1_deq_6_index_0_at_time_1 -> 
 Implies(And(7 - cpu_cap_cnt_at_time_1 > 0,
            cpu_deq_cnt_at_time_0 == 6),
        And(cpu_index_6_time_0_val == cpu_index_0_time_1_val,
            cpu_index_6_time_0_src == cpu_index_0_time_1_src,
            cpu_index_6_time_0_loc == cpu_index_0_time_1_loc,
            cpu_index_6_time_0_stime ==
            cpu_index_0_time_1_stime))
cons_for_cpu_flow_control_3_index_1_at_time_1 -> 
 Implies(7 - cpu_cap_cnt_at_time_1 + cpu_input_cnt_at_time_1 <=
        1,
        Not(cpu_index_1_time_1_val))
cons_for_cpu_flow_control_3_index_2_at_time_1 -> 
 Implies(7 - cpu_cap_cnt_at_time_1 + cpu_input_cnt_at_time_1 <=
        2,
        Not(cpu_index_2_time_1_val))
cons_for_cpu_flow_control_3_index_3_at_time_1 -> 
 Implies(7 - cpu_cap_cnt_at_time_1 + cpu_input_cnt_at_time_1 <=
        3,
        Not(cpu_index_3_time_1_val))
cons_for_cpu_flow_control_3_index_4_at_time_1 -> 
 Implies(7 - cpu_cap_cnt_at_time_1 + cpu_input_cnt_at_time_1 <=
        4,
        Not(cpu_index_4_time_1_val))
cons_for_cpu_flow_control_3_index_5_at_time_1 -> 
 Implies(7 - cpu_cap_cnt_at_time_1 + cpu_input_cnt_at_time_1 <=
        5,
        Not(cpu_index_5_time_1_val))
cons_for_cpu_flow_control_3_index_6_at_time_1 -> 
 Implies(7 - cpu_cap_cnt_at_time_1 + cpu_input_cnt_at_time_1 <=
        6,
        Not(cpu_index_6_time_1_val))
cons_for_cpu_flow_control_3_index_0_at_time_2 -> 
 Implies(7 - cpu_cap_cnt_at_time_2 + cpu_input_cnt_at_time_2 <=
        0,
        Not(cpu_index_0_time_2_val))
cons_for_cpu_flow_control_3_index_1_at_time_2 -> 
 Implies(7 - cpu_cap_cnt_at_time_2 + cpu_input_cnt_at_time_2 <=
        1,
        Not(cpu_index_1_time_2_val))
cons_for_cpu_flow_control_3_index_2_at_time_2 -> 
 Implies(7 - cpu_cap_cnt_at_time_2 + cpu_input_cnt_at_time_2 <=
        2,
        Not(cpu_index_2_time_2_val))
cons_for_cpu_flow_control_3_index_3_at_time_2 -> 
 Implies(7 - cpu_cap_cnt_at_time_2 + cpu_input_cnt_at_time_2 <=
        3,
        Not(cpu_index_3_time_2_val))
cons_for_cpu_flow_control_3_index_4_at_time_2 -> 
 Implies(7 - cpu_cap_cnt_at_time_2 + cpu_input_cnt_at_time_2 <=
        4,
        Not(cpu_index_4_time_2_val))
cons_for_cpu_flow_control_3_index_5_at_time_2 -> 
 Implies(7 - cpu_cap_cnt_at_time_2 + cpu_input_cnt_at_time_2 <=
        5,
        Not(cpu_index_5_time_2_val))
cons_for_cpu_flow_control_3_index_6_at_time_2 -> 
 Implies(7 - cpu_cap_cnt_at_time_2 + cpu_input_cnt_at_time_2 <=
        6,
        Not(cpu_index_6_time_2_val))
cons_mc_self_deq_cnt_at_time_2 -> 
 If(mc_val_cnt_at_time_2 > 4,
   mc_deq_cnt_at_time_2 == 4,
   mc_deq_cnt_at_time_2 == mc_val_cnt_at_time_2)
cons_mc_self_deq_cnt_at_time_3 -> 
 If(mc_val_cnt_at_time_3 > 4,
   mc_deq_cnt_at_time_3 == 4,
   mc_deq_cnt_at_time_3 == mc_val_cnt_at_time_3)
set_max_input_for_cpu -> 
 And(If(cpu_credit_cnt_at_time_0 < cpu_cap_cnt_at_time_0,
       cpu_input_cnt_at_time_0 == cpu_credit_cnt_at_time_0,
       cpu_input_cnt_at_time_0 == cpu_cap_cnt_at_time_0),
    If(cpu_credit_cnt_at_time_1 < cpu_cap_cnt_at_time_1,
       cpu_input_cnt_at_time_1 == cpu_credit_cnt_at_time_1,
       cpu_input_cnt_at_time_1 == cpu_cap_cnt_at_time_1),
    If(cpu_credit_cnt_at_time_2 < cpu_cap_cnt_at_time_2,
       cpu_input_cnt_at_time_2 == cpu_credit_cnt_at_time_2,
       cpu_input_cnt_at_time_2 == cpu_cap_cnt_at_time_2),
    If(cpu_credit_cnt_at_time_3 < cpu_cap_cnt_at_time_3,
       cpu_input_cnt_at_time_3 == cpu_credit_cnt_at_time_3,
       cpu_input_cnt_at_time_3 == cpu_cap_cnt_at_time_3),
    If(cpu_credit_cnt_at_time_4 < cpu_cap_cnt_at_time_4,
       cpu_input_cnt_at_time_4 == cpu_credit_cnt_at_time_4,
       cpu_input_cnt_at_time_4 == cpu_cap_cnt_at_time_4),
    If(cpu_credit_cnt_at_time_5 < cpu_cap_cnt_at_time_5,
       cpu_input_cnt_at_time_5 == cpu_credit_cnt_at_time_5,
       cpu_input_cnt_at_time_5 == cpu_cap_cnt_at_time_5))
set_cache_replace_cnt_for_llc -> 
 If(llc_replace_index_0_at_time_0, 1, 0) +
If(llc_replace_index_1_at_time_0, 1, 0) +
If(llc_replace_index_2_at_time_0, 1, 0) +
If(llc_replace_index_3_at_time_0, 1, 0) +
If(llc_replace_index_0_at_time_1, 1, 0) +
If(llc_replace_index_1_at_time_1, 1, 0) +
If(llc_replace_index_2_at_time_1, 1, 0) +
If(llc_replace_index_3_at_time_1, 1, 0) +
If(llc_replace_index_0_at_time_2, 1, 0) +
If(llc_replace_index_1_at_time_2, 1, 0) +
If(llc_replace_index_2_at_time_2, 1, 0) +
If(llc_replace_index_3_at_time_2, 1, 0) +
If(llc_replace_index_0_at_time_3, 1, 0) +
If(llc_replace_index_1_at_time_3, 1, 0) +
If(llc_replace_index_2_at_time_3, 1, 0) +
If(llc_replace_index_3_at_time_3, 1, 0) +
If(llc_replace_index_0_at_time_4, 1, 0) +
If(llc_replace_index_1_at_time_4, 1, 0) +
If(llc_replace_index_2_at_time_4, 1, 0) +
If(llc_replace_index_3_at_time_4, 1, 0) +
If(llc_replace_index_0_at_time_5, 1, 0) +
If(llc_replace_index_1_at_time_5, 1, 0) +
If(llc_replace_index_2_at_time_5, 1, 0) +
If(llc_replace_index_3_at_time_5, 1, 0) >=
12
