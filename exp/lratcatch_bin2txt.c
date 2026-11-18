/* lratcatch_bin2txt.c (research only; untrusted plumbing): binary LRAT on stdin -> text LRAT on stdout, streaming.
 *
 * Input: the binary LRAT that CaDiCaL --binary=true, lrat-trim and code/ccc90.py (ext_cube segments, stitch) write:
 *   'a' (0x61) id lit... 0 hint... 0      addition; id = 2*i, lit = 2*|l| + (l<0), hint = 2*h (+1 for a RAT hint, h<0)
 *   'd' (0x64) id... 0                    deletion; id = 2*i
 * every number an unsigned LEB128 varint (ccc90.py rv/wv).
 * Output: one text line per action, ids and hints kept exactly as in the input (renumbering is left to
 * lratcatch-compact-renumber, which maps any id to the checker's compacted positions):
 *   "<i> <lits> 0 <hints> 0"   and   "<last addition id> d <ids> 0"
 * No comment or empty line is ever written: the lrat-catcher feed and compact-renumber both count lines.
 *
 * Nothing here is trusted: lrat-catcher's theorem is about the CNF only and holds for whatever stream is checked; a
 * wrong conversion can only make the check fail.
 *
 * Usage: lratcatch_bin2txt CNF_MAXVAR FIRST_DEL_ID STATS.json < proof.bin > proof.txt
 *   CNF_MAXVAR: largest variable of the base CNF; a literal above it stops the run (exit 3): lrat-catcher's checker
 *   works over the CNF's variables only (no extension variables), so such a proof could not be checked.
 *   FIRST_DEL_ID: id printed on deletion lines before the first addition (use the number of base clauses).
 * Exit 0 ok, 2 malformed input, 3 variable out of range, 4 output closed or write error, 5 interrupted (SIGINT/TERM). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <signal.h>

static unsigned char ibuf[1 << 20]; static size_t ilen = 0, ipos = 0; static uint64_t inbytes = 0;
static char obuf[1 << 22]; static size_t opos = 0;
static volatile sig_atomic_t stop_req = 0;
static void on_sig(int s) { (void)s; stop_req = 1; }

static int getb(void) {
  if (ipos == ilen) {
    if (stop_req) return -2;
    ilen = fread(ibuf, 1, sizeof ibuf, stdin); ipos = 0;
    if (ilen == 0) return -1;
    inbytes += ilen;
  }
  return ibuf[ipos++];
}
static int out_err = 0;
static void flush_out(void) {   /* a closed reader (the checker stops after the empty clause) ends the run, exit 4 */
  if (opos && !out_err && fwrite(obuf, 1, opos, stdout) != opos) { out_err = 1; stop_req = 1; }
  opos = 0;
}
static inline void putc_o(char c) { if (opos == sizeof obuf) flush_out(); obuf[opos++] = c; }
static inline void put_u(uint64_t x) {
  char t[24]; int n = 0;
  do { t[n++] = (char)('0' + x % 10); x /= 10; } while (x);
  if (opos + 24 > sizeof obuf) flush_out();
  while (n) obuf[opos++] = t[--n];
}
static inline void put_i(int64_t x) { if (x < 0) { putc_o('-'); put_u((uint64_t)(-x)); } else put_u((uint64_t)x); }
static int bad(const char *m, uint64_t at) { flush_out(); fprintf(stderr, "bin2txt: %s at input byte %llu\n", m, (unsigned long long)at); return 2; }

/* read one varint; returns 0 ok, -1 eof at start, -2 eof inside, -3 overflow */
static int rv(uint64_t *x) {
  uint64_t v = 0; int s = 0; int c = getb();
  if (c == -1) return -1;
  if (c == -2) return -4;
  for (;;) {
    if (s > 63) return -3;
    v |= (uint64_t)(c & 0x7f) << s; s += 7;
    if (c < 0x80) { *x = v; return 0; }
    c = getb(); if (c < 0) return c == -2 ? -4 : -2;
  }
}

int main(int argc, char **argv) {
  if (argc != 4) { fprintf(stderr, "usage: lratcatch_bin2txt CNF_MAXVAR FIRST_DEL_ID STATS.json < bin > txt\n"); return 2; }
  uint64_t maxvar_cnf = strtoull(argv[1], 0, 10), cur = strtoull(argv[2], 0, 10);
  signal(SIGINT, on_sig); signal(SIGTERM, on_sig); signal(SIGPIPE, SIG_IGN);
  uint64_t adds = 0, dels = 0, delids = 0, lits = 0, hints = 0, rat = 0, lines = 0, maxvar = 0, maxid = 0;
  uint64_t nonmono = 0, prev = 0, empties = 0; int64_t live = 0, peaklive = 0; int rc = 0;
  for (;;) {
    int t = getb();
    if (t == -1) break;
    if (t == -2) { rc = 5; break; }
    uint64_t at = inbytes - (ilen - ipos) - 1, x; int r;
    if (t == 0x61) {
      if ((r = rv(&x)) != 0) { rc = r == -4 ? 5 : bad("truncated addition id", at); break; }
      if (x & 1) { rc = bad("negative addition id", at); break; }
      uint64_t id = x >> 1; if (id > maxid) maxid = id;
      if (id <= prev) nonmono++;
      prev = id; cur = id; put_u(id); int n = 0;
      for (;;) {
        if ((r = rv(&x)) != 0) { rc = r == -4 ? 5 : bad("truncated clause", at); goto out; }
        if (x == 0) break;
        uint64_t v = x >> 1; if (v == 0) { rc = bad("variable 0", at); goto out; }
        if (v > maxvar) maxvar = v;
        if (v > maxvar_cnf) { flush_out(); fprintf(stderr, "bin2txt: variable %llu above the CNF's %llu (extension variable)\n", (unsigned long long)v, (unsigned long long)maxvar_cnf); rc = 3; goto out; }
        putc_o(' '); if (x & 1) putc_o('-'); put_u(v); lits++; n++;
      }
      if (!n) empties++;
      putc_o(' '); putc_o('0');
      for (;;) {
        if ((r = rv(&x)) != 0) { rc = r == -4 ? 5 : bad("truncated hints", at); goto out; }
        if (x == 0) break;
        putc_o(' '); if (x & 1) { putc_o('-'); rat++; } put_u(x >> 1); hints++;
      }
      putc_o(' '); putc_o('0'); putc_o('\n'); adds++; lines++; live++; if (live > peaklive) peaklive = live;
    } else if (t == 0x64) {
      put_u(cur); putc_o(' '); putc_o('d');
      for (;;) {
        if ((r = rv(&x)) != 0) { rc = r == -4 ? 5 : bad("truncated deletion", at); goto out; }
        if (x == 0) break;
        if (x & 1) { rc = bad("negative deletion id", at); goto out; }
        putc_o(' '); put_u(x >> 1); delids++; live--;
      }
      putc_o(' '); putc_o('0'); putc_o('\n'); dels++; lines++;
    } else { rc = bad("unknown action byte", at); break; }
  }
out:
  flush_out(); if (fflush(stdout) != 0) out_err = 1;
  if (out_err && (rc == 0 || rc == 5)) rc = 4;
  FILE *f = fopen(argv[3], "w");
  if (f) {
    fprintf(f, "{\"exit\": %d, \"interrupted\": %s, \"output_closed\": %s, \"input_bytes\": %llu, \"lines\": %llu, \"additions\": %llu, \"deletion_lines\": %llu, "
               "\"deleted_ids\": %llu, \"literals\": %llu, \"hints\": %llu, \"rat_hints\": %llu, \"empty_clauses\": %llu, "
               "\"max_var\": %llu, \"cnf_max_var\": %llu, \"max_id\": %llu, \"non_increasing_ids\": %llu, "
               "\"peak_added_minus_deleted\": %lld}\n",
            rc, (rc == 5 && !out_err) ? "true" : "false", out_err ? "true" : "false", (unsigned long long)inbytes, (unsigned long long)lines, (unsigned long long)adds,
            (unsigned long long)dels, (unsigned long long)delids, (unsigned long long)lits, (unsigned long long)hints,
            (unsigned long long)rat, (unsigned long long)empties, (unsigned long long)maxvar, (unsigned long long)maxvar_cnf,
            (unsigned long long)maxid, (unsigned long long)nonmono, (long long)peaklive);
    fclose(f);
  }
  return rc;
}
