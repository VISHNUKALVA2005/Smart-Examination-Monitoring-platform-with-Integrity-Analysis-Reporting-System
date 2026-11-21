"""Generate reproducible-looking synthetic session log rows for Milestone 1 demo."""
import argparse, csv, random
from datetime import datetime, timedelta
from faker import Faker
fake = Faker()
EVENTS = ["SESSION_STARTED", "SESSION_PAUSED", "SESSION_RESUMED", "SESSION_SUBMITTED", "FOCUS_LOST", "TAB_SWITCH"]

def generate(count=50, output="synthetic_session_logs.csv", seed=42):
    random.seed(seed); Faker.seed(seed)
    rows=[]; now=datetime.now()
    for i in range(1, count+1):
        start=now-timedelta(days=random.randint(0,14), hours=random.randint(0,8))
        event=random.choice(EVENTS)
        rows.append({"synthetic_session_id": f"SYN-{i:04d}", "candidate_name": fake.name(), "candidate_email": fake.email(), "event_type": event, "description": f"Synthetic demonstration event: {event.lower().replace('_',' ')}", "occurred_at": (start+timedelta(minutes=random.randint(0,120))).isoformat(timespec="seconds")})
    with open(output,"w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    return output
if __name__ == "__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--count",type=int,default=50); parser.add_argument("--output",default="synthetic_session_logs.csv"); args=parser.parse_args()
    print(f"Generated {args.count} synthetic records: {generate(args.count,args.output)}")
