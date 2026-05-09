import re
from dataclasses import dataclass
import sys

@dataclass
class CountSummary:
    tot_cnt: int
    invalid_cnt: int
    error_cnt: int
    warn_cnt: int
    info_cnt: int

@dataclass
class LogLines:
    error_msgs: list
    warn_msgs: list
    info_msgs: list
    invalid_lines: list

log_pattern = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(?P<level>INFO|ERROR|WARNING) "
    r"(?P<message>.*)$"
)


def parse_log_line(line):
    match = log_pattern.match(line)  
    if not match:
        return None
    return match.groupdict()

def read_file(filename):
    while True:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
                return lines
        except FileNotFoundError:
            filename = input("File not found. Enter correct filename (or press Enter to quit): ").strip()
            if not filename:
                return None

def get_counts(lines):
    tot_cnt = 0
    invalid_cnt = 0
    info_cnt = 0
    warn_cnt = 0
    error_cnt = 0
    error_lines = []
    invalid_lines = []
    warn_lines = []
    info_lines = []
    for line in lines:
        tot_cnt += 1
        parsed_line = parse_log_line(line)
        if parsed_line is None :
            invalid_cnt += 1
            invalid_lines.append(line)
            continue
        if parsed_line.get("level") == "WARNING" : 
            warn_cnt += 1
            warn_lines.append(line)
        elif parsed_line.get("level") == "ERROR" :
            error_cnt += 1
            error_lines.append(line)
        elif parsed_line.get("level") == "INFO" :
            info_cnt += 1
            info_lines.append(line)
    return CountSummary(tot_cnt, invalid_cnt, error_cnt, warn_cnt, info_cnt), LogLines(error_lines, warn_lines, info_lines, invalid_lines)


if __name__ == "__main__":
    lines = read_file("log.txt")
    summary_cnt,msg_lines = get_counts(lines)

    print(f"Total log lines           : {summary_cnt.tot_cnt}")
    print(f"Total valid log entries   : {summary_cnt.tot_cnt - summary_cnt.invalid_cnt}")
    print(f"Malformed log entries     : {summary_cnt.invalid_cnt}")
    print(f"Error : {summary_cnt.error_cnt}.   \nWarning : {summary_cnt.warn_cnt}.    \nInfo : {summary_cnt.info_cnt}")
    print("Errors : \n", "".join(msg_lines.error_msgs))
    print("Invalid lines. : \n","".join(msg_lines.invalid_lines))
   
        





        ###
#        ========== LOG FILE SUMMARY ==========

#Total log lines        : 6
#Valid log entries      : 5
#Malformed log entries  : 1

#---------- Log Level Counts ----------

#INFO     : 2
#WARNING  : 1
#ERROR    : 2

#---------- ERROR MESSAGES ------------

#1. 2026-05-08 10:16:10 ERROR Database connection failed

#2. 2026-05-08 10:20:11 ERROR Timeout while calling API

#---------- MALFORMED LINES -----------

#1. INVALID LOG LINE

#======================================